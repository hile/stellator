"""
Virtual machine configuration
"""

import glob
import os

from stellator.constants import *
from stellator.fileparser import VMWareConfigFileParser, IndexedConfigEntry, FileParserError
from stellator.util import arp_resolve_ip_address


class VirtualMachineError(Exception):
    pass


class VirtualMachineConfigurationSection(IndexedConfigEntry):
    """Common dot separated config section

    Parse keys in configuration and set to attributes of the object.
    """
    integer_keys = ()
    boolean_keys = ()
    key_map = {}

    def __init__(self, virtualmachine, index):
        super(VirtualMachineConfigurationSection, self).__init__(index)
        self.virtualmachine = virtualmachine

    def set(self, parts, value):
        if len(parts) > 1:
            return parts, value

        key = parts[0]

        if key in self.integer_keys:
            value = int(value)

        if key in self.boolean_keys:
            value = value == 'TRUE'

        if key in self.key_map:
            key = self.key_map[key]

        setattr(self, key, value)
        return key, value


class Interface(VirtualMachineConfigurationSection):
    """Ethernet network interface

    Virtualmachine Ethernet network interface
    """
    integer_keys = ( 'pciSlotNumber', 'generatedAddressOffset', )
    boolean_keys = ( 'present', 'startConnected', 'wakeOnPcktRcv', )
    key_map =  {
        'virtualDev': 'driver',
        'connectionType': 'connection_type',
        'startConnected': 'start_connected',
        'generatedAddress': 'mac_address',
        'wakeOnPcktRcv': 'wake_on_packet_receive',
        'addressType': 'address_type',
        'generatedAddressOffset': 'generated_address_offset',
        'pciSlotNumber': 'pci_slot_number',
    }

    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        self.driver = 'unknown'

    @property
    def autoconnect(self):
        if not hasattr(self, 'start_connected'):
            return False
        return self.start_connected

    @property
    def ip_address(self):
        """Resolve IP

        Returns IP address from ARP table or None
        """
        return arp_resolve_ip_address(self.mac_address)


class PCIBridge(VirtualMachineConfigurationSection):
    """PCI bridge

    Virtualmachine PCI bridge
    """
    integer_keys = ( 'pciSlotNumber', 'functions', )
    boolean_keys = ( 'present', )
    key_map =  { 'virtualDev': 'virtual_device', 'pciSlotNumber': 'pci_slot_number', }


class USBPort(VirtualMachineConfigurationSection):
    """USB port

    Virtualmachine USB port attached
    """
    integer_keys = ( 'parent', 'speed', 'port', )
    boolean_keys = ( 'present', )
    key_map = { 'deviceType': 'device_type', }


class USB(VirtualMachineConfigurationSection):
    """USB support

    Section for USB support in VMs. Contains USBPort objects as well.
    """
    integer_keys = ( 'pciSlotNumber', )
    boolean_keys = ( 'present', )
    key_map = { 'pciSlotNumber': 'pci_slot_number', }

    def __init__(self, virtualmachine, index=0):
        super(USB, self).__init__(virtualmachine, index)
        self.interfaces = []

class Share(VirtualMachineConfigurationSection):
    """Mapped shared folder

    """
    boolean_keys = ( 'enabled', 'present', 'readAccess', 'writeAccess', )
    key_map = {
        'hostPath':     'host_path',
        'guestName':    'guest_folder_name',
        'readAccess':   'guest_read_access',
        'writeAccess':  'guest_write_access',
    }


class SharedFolders(VirtualMachineConfigurationSection):
    """Shared folder configuration

    """
    def __init__(self, virtualmachine, index=0):
        super(SharedFolders, self).__init__(virtualmachine, index)
        self.shares = []

    integer_keys = ( 'maxNum', )
    key_map = { 'maxNum': 'max_number', }


class VMCI(VirtualMachineConfigurationSection):
    """VMCI

    """
    integer_keys = ( 'pciSlotNumber', )
    boolean_keys = ( 'present', )
    key_map = { 'pciSlotNumber': 'pci_slot_number', }


class VirtualMachine(VMWareConfigFileParser):
    """Vmware .vmx parser

    Parse .vmx file and give some functionality to control the VM.
    """
    def __init__(self, inventory, path):
        super(VirtualMachine, self).__init__(path)

        self.inventory = inventory

        # Set defaults for keys
        for key, value in VMX_KEY_MAP.items():
            if key in VMX_INTEGER_KEYS:
                setattr(self, value, 0)
            else:
                setattr(self, value, None)

        self.interfaces = []
        self.pci_bridges = []
        self.vmci_interfaces = []
        self.blockdevices = []

        self.shared_folders = SharedFolders(self)
        self.usb = USB(self)

        try:
            self.load()
        except FileParserError as e:
            raise VirtualMachineError('Error loading {0}: {1}'.format(self.path, e))

    def __repr__(self):
        return self.path

    def __cmp__(self, other):
        return cmp(self.path, other.path)

    @property
    def description(self):
        value = self.annotation
        if value is None:
            return ''
        return '\n'.join(value.split('|0A'))

    @property
    def directory(self):
        """Return .vmx directory

        Return directory where .vmx file is
        """
        return os.path.dirname(self.path)

    @property
    def headless(self):
        """Is VM headless

        Headless VMs are not shown in GUI but can be run with vmrun and nogui
        """
        return self.inventory.find_vmx(self.path) is None

    @property
    def is_running(self):
        """Is VM running

        """
        try:
            running_vms = self.inventory.vmrun.running_vms()
        except VMRunError, emsg:
            # TODO - maybe we want something else here?
            raise VMRunError(emsg)

        return self.path in running_vms

    @property
    def autoresume_file(self):
        """Filename for autoresume

        Internal file to mark autoresume for VM.
        """
        return os.path.join(self.directory, self.inventory.config['autoresume_filename'])

    @property
    def autoresume(self):
        """Is VM autoresuming

        True if self.autoresume_file exists
        """
        return os.path.isfile(self.autoresume_file)

    @property
    def has_vmem(self):
        """Has .vmem file

        If VM is not running and has .vmem files, it is suspended.
        """
        return len(glob.glob('{0}/*.vmem'.format(self.directory))) > 0

    @property
    def status(self):
        """Return status string

        Returns status string for VM
        """
        if self.inventory.is_running(self):
            return 'running'

        elif self.has_vmem:
            return 'suspended'

        return 'stopped'

    def start(self):
        """Start VM

        """
        if self.is_running:
            return

        self.inventory.vmrun.start(self.path, headless=self.headless)

        if os.path.isfile(self.autoresume_file):
            try:
                os.unlink(self.autoresume_file)
            except OSError, (ecode, emsg):
                pass
            except OSError, (ecode, emsg):
                pass

    def suspend(self, autoresume=False):
        """Suspend VM

        If autoresume is True, a file is touched that allows scripts to
        resume the script automatically, for example after hibernation.

        This applies only to  headless VMs.
        """
        if not self.is_running:
            return

        self.inventory.vmrun.suspend(self.path)

        if autoresume and self.headless:
            try:
                open(self.autoresume_file, 'w').write('\n')
            except OSError, (ecode, emsg):
                pass
            except OSError, (ecode, emsg):
                pass

    def stop(self):
        """Stop VM

        Stop (shutdown) the VM
        """
        if not self.is_running:
            return

        self.inventory.vmrun.stop(self.path)

    def __get_interface__(self, index):
        for interface in self.interfaces:
            if interface == index:
                return interface

        interface = Interface(self, index)
        self.interfaces.append(interface)
        return interface

    def __get_vmci__(self, index):
        for vmci in self.vmci_interfaces:
            if vmci == index:
                return vmci

        vmci = VMCI(self, index)
        self.vmci_interfaces.append(vmci)
        return vmci

    def __get_pci_bridge__(self, index):
        for bridge in self.pci_bridges:
            if bridge == index:
                return bridge

        bridge = PCIBridge(self, index)
        self.pci_bridges.append(bridge)
        return bridge

    def __get_usb_interface__(self, index):
        for interface in self.usb.interfaces:
            if interface == index:
                return interface

        interface = USBPort(self, index)
        self.usb.interfaces.append(interface)
        return interface

    def __get_share__(self, index):
        for share in self.shared_folders.shares:
            if share.index == index:
                return share

        share = Share(self, index)
        self.shared_folders.shares.append(share)
        return share

    def parse_value(self, key, value):
        """Parse values

        Right now we skip most keys: implement rest if you are interested.
        """
        if super(VirtualMachine, self).parse_value(key, value):
            return

        if key in VMX_BOOLEAN_KEYS:
            value = value == 'TRUE'

        if key in VMX_INTEGER_KEYS:
            value = int(value)

        if key in VMX_KEY_MAP:
            key = VMX_KEY_MAP[key]
            setattr(self, key, value)

        else:
            parts = key.split('.')

            if parts[0] == 'usb':
                self.usb.set(parts[1:], value)

            elif parts[0][:4] == 'vmci':
                index = int(parts[0][4:])
                parts = parts[1:]
                vmci = self.__get_vmci__(index)
                vmci.set(parts, value)

            elif parts[0][:8] == 'ethernet':
                index = int(parts[0][8:])
                parts = parts[1:]
                interface = self.__get_interface__(index)
                interface.set(parts, value)

            elif parts[0][:9] == 'pciBridge':
                index = int(parts[0][9:])
                parts = parts[1:]
                bridge = self.__get_pci_bridge__(index)
                bridge.set(parts, value)

            elif parts[0][:4] == 'usb:':
                try:
                    index = int(parts[0][4:])
                    parts = parts[1:]
                    usb = self.__get_usb_interface__(index)
                    usb.set(parts, value)
                except ValueError:
                    print parts

            elif key == 'sharedFolder.maxNum':
                self.shared_folders.count = value

            elif parts[0][:12] == 'sharedFolder':
                try:
                    index = int(parts[0][12:])
                    parts = parts[1:]
                    share = self.__get_share__(index)
                    share.set(parts, value)
                except ValueError, emsg:
                    print parts

            else:
                pass
                # TODO - parse rest of options: these are not really interesting
                #print '{0}\n  {1} {2}'.format(key, type(value), value)
