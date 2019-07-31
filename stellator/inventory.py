"""
Parser for user's vmware fusion virtual machine inventory
"""

import fnmatch
import os

from .config import StellatorConfig
from .constants import (
    INVENTORY_VM_BOOLEAN_FLAG_KEYS,
    INVENTORY_VM_INTEGER_KEYS,
    INVENTORY_VM_KEY_MAP,
)
from .fileparser import VMWareConfigFileParser, IndexedConfigEntry
from .virtualmachine import VirtualMachine, VirtualMachineError
from .vmrun import VMRunWrapper


class InventoryIndexField(IndexedConfigEntry):
    """Field for index

    Setting field for index
    """
    def __init__(self, inventory_index, index):
        super(InventoryIndexField, self).__init__(index)
        self.inventory_index = inventory_index

        self.default = False
        self.name = None
        self.value = None

    def __repr__(self):
        return '{} {} {}'.format(self.inventory_index, self.name, self.value)

    def set(self, key, value):
        if key == 'default':
            self.default = value == 'True'
        else:
            setattr(self, key, value)


class InventoryIndex(IndexedConfigEntry):
    """Sortable inventory index

    Indexes the VMs shown in GUI
    """
    def __init__(self, inventory, index):
        super(InventoryIndex, self).__init__(index)

        self.inventory = inventory
        self.host_id = None
        self.vmx_path = None

        self.field_count = 0
        self.fields = []

    def __repr__(self):
        return '{} {} {}'.format(self.index, self.host_id, self.vmx_path)

    def __get_field__(self, index):
        for instance in self.fields:
            if instance == index:
                return instance

        instance = InventoryIndexField(self, index)
        self.fields.append(instance)
        return instance

    @property
    def vmx_config(self):
        """Return VM config matching index

        """
        return self.inventory.find_vmx(self.vmx_path)

    def set(self, parts, value):
        if parts == ['id']:
            self.vmx_path = value

        elif parts == ['hostID']:
            self.host_id = value

        elif parts == ['field', 'count']:
            self.field_count = int(value)

        elif parts[0][:5] == 'field':
            field_index = int(parts[0][5:])
            key = '.'.join(parts[1:])
            field = self.__get_field__(field_index)
            field.set(key, value)

        else:
            print(self, parts, value)


class InventoryVirtualMachine(IndexedConfigEntry):
    """VM config in inventory

    Details for VM in inventory file. Virtualmachine object is in
    self.virtualmachine property.
    """
    def __init__(self, inventory, index):
        super(InventoryVirtualMachine, self).__init__(index)

        self.inventory = inventory
        self.vmx_path = None
        self.virtual_folder = False

        self.config = {
            'name': 'unknown',
        }

    def __repr__(self):
        return '{} {}'.format(self.config['name'], self.vmx_path)

    @property
    def virtualmachine(self):
        return VirtualMachine(self.inventory, self.vmx_path)

    def set(self, parts, value):
        key = '.'.join(parts)

        if key in INVENTORY_VM_BOOLEAN_FLAG_KEYS:
            value = value == 'TRUE'

        if key in INVENTORY_VM_INTEGER_KEYS:
            value = int(value)

        if key == 'UUID':
            value = value.replace(' ', '')

        if key == 'config':
            if value != '':
                self.vmx_path = value

        elif key in INVENTORY_VM_KEY_MAP:
            self.config[INVENTORY_VM_KEY_MAP[key]] = value

        elif key == 'Type' and value == '2':
            self.virtual_folder = True

        elif key == 'Expanded':
            # Virtual folder state, not intresting
            pass

        else:
            print('unknown key', self, key, value)


class Inventory(VMWareConfigFileParser):
    """VM inventory

    Inventory used by the GUI
    """
    def __init__(self, config):
        super(Inventory, self).__init__(config['inventory'])
        self.config = config
        self.vmrun = VMRunWrapper(self.config)
        self.index_count = 0

        self.indexes = []
        self.vmx_configs = []

        self.running_vms = []
        self.__running_vms_loaded = False

        self.load()

    def __get_index__(self, index):
        for instance in self.indexes:
            if instance == index:
                return instance

        instance = InventoryIndex(self, index)
        self.indexes.append(instance)
        return instance

    def __get_virtualmachine__(self, index):
        for instance in self.vmx_configs:
            if instance == index:
                return instance

        instance = InventoryVirtualMachine(self, index)
        self.vmx_configs.append(instance)
        return instance

    def __cleanup__vms__(self):
        for vm in [vm for vm in self.vmx_configs]:
            if vm.vmx_path is None:
                self.vmx_configs.remove(vm)
            if vm.virtual_folder:
                self.vmx_configs.remove(vm)
        self.vmx_configs.sort()

    @property
    def virtualmachines(self):
        """Return virtualmachines

        Return VMs matching the inventory config
        """
        virtualmachines = []
        for config in self.vmx_configs:
            try:
                virtualmachines.append(config.virtualmachine)
            except VirtualMachineError as e:
                print('Error loading {}: {}'.format(config, e))

        return virtualmachines

    def update_running_vmx(self):
        """Update list of running VMs

        Update running VMs list
        """
        self.running_vms = self.vmrun.running_vms()
        self.__running_vms_loaded = True

    def is_running(self, virtualmachine):
        """Check if VM is running

        This uses cached .running_vms - to update, run update_running_vmx() first.
        """
        if not self.__running_vms_loaded:
            self.update_running_vmx()
        return virtualmachine.path in self.running_vms

    def load(self):
        """Load inventory

        """
        rv = super(Inventory, self).load()
        self.indexes.sort()
        self.__cleanup__vms__()

        return rv

    def parse_value(self, key, value):
        """Parse values

        Parses inventory file values
        """
        if super(Inventory, self).parse_value(key, value):
            return

        elif key == 'index.count':
            self.index_count = int(value)
            return

        # Parse key prefix and index
        parts = key.split('.')

        if parts[0][:5] == 'index':
            index = int(parts[0][5:])
            parts = parts[1:]
            index = self.__get_index__(index)
            index.set(parts, value)

        if parts[0][:6] == 'vmlist':
            index = int(parts[0][6:])
            parts = parts[1:]
            virtualmachine = self.__get_virtualmachine__(index)
            virtualmachine.set(parts, value)

    def find_vmx(self, vmx_path):
        """Find vmx from inventory

        Returns vmx_config that matches path or None
        """
        for config in self.vmx_configs:
            if config.vmx_path == vmx_path:
                return config
        return None


class VirtualMachineFinder(list):
    """Find vmware virtual machines

    Find virtual machines both in specified path or in fusion inventory.

    Path defaults to DEFAULT_VMWARE_DIRECTORY, which either is taken from
    VMWARE_DIRECTORY environment variable or defaults to user's default
    VM location ~/Documents/Virtual Machines.localized.
    """

    def __init__(self, config=None):
        if config is None:
            config = StellatorConfig()
        self.config = config

        self.inventory = Inventory(config)
        self.path = config['virtualmachines_path']
        self.load()

    def is_running(self, virtualmachine):
        """Check if VM is running

        """
        return self.inventory.is_running(virtualmachine)

    def match_vm_names(self, patterns, case_sensitive=False):
        """Match VM names to patterns

        Return virtual machines that match the specified glob patterns.

        The match is case insensitive.
        """

        matches = []

        for virtualmachine in self:

            for pattern in patterns:
                if case_sensitive:
                    if fnmatch.fnmatch(virtualmachine.name, pattern):
                        matches.append(virtualmachine)
                        break
                else:
                    if fnmatch.fnmatch(virtualmachine.name.lower(), pattern.lower()):
                        matches.append(virtualmachine)
                        break

        return matches

    def load(self):
        """Load virtual machines

        Load virtual machines from directory and inventory
        """

        for root, _dirs, files in os.walk(self.path):
            for filename in files:
                if os.path.splitext(filename)[1] == '.vmx':
                    self.append(VirtualMachine(self.inventory, os.path.join(root, filename)))

        for vm in self.inventory.virtualmachines:
            if vm not in self:
                self.append(vm)

        return [vm for vm in self]
