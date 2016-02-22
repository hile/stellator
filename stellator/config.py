"""
Stellator configuration file parsing
"""

import configobj
import os

CONFIG_DIRECTORY = os.path.expanduser('~/Library/Application Support/Stellator')
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIRECTORY, 'stellator.conf')


# Paths to vmware fusion install locations
VMWARE_FUSION_PATHS = (
    os.path.expanduser('~/Applications/VMware Fusion.app'),
    '/Applications/VMware Fusion.app',
)

def detect_vmware_fusion():
    for path in VMWARE_FUSION_PATHS:
        if os.path.isdir(path):
            return path
    raise StellatorConfigError('Could not detect installed vmware fusion')


DEFAULT_CONFIG = {
    'inventory': os.path.expanduser('~/Library/Application Support/VMware Fusion/vmInventory'),
    'application_path': detect_vmware_fusion(),
    'autoresume_filename': 'autoresume.stellator',
    'virtualmachines_path': os.path.expanduser('~/Documents/Virtual Machines.localized'),
}


class StellatorConfigError(Exception):
    pass


class StellatorConfig(dict):
    """User configuration

    Configuration file is in ~/Library/Application Support/Stellator/stellator.conf.
    Usually not needed but if you so wish, you can override things there. The default
    settings from DEFAULT_CONFIG should work.

    Note: following environment variables always overrides settings in config:

        VMWARE_INVENTORY: inventory
        VMWARE_DIRECTORY: virtualmachines_path

    """
    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.path = path

        self.update(DEFAULT_CONFIG)
        self.load()

        # Read environment and override settings if needed
        vm_inventory = os.environ.get('VMWARE_INVENTORY', None)
        if vm_inventory:
            self['inventory'] = vm_inventory

        vm_directory = os.environ.get('VMWARE_DIRECTORY', None)
        if vm_directory:
            self['virtualmachines_path'] = vm_directory

    def load(self):
        """Load user configuration

        """
        if not os.path.isdir(CONFIG_DIRECTORY):
            try:
                os.makedirs(CONFIG_DIRECTORY)
            except OSError, (ecode, emsg):
                raise StellatorConfigError('Error creating directory {0}: {1}'.format(CONFIG_DIRECTORY, emsg))
            except IOError, (ecode, emsg):
                raise StellatorConfigError('Error creating directory {0}: {1}'.format(CONFIG_DIRECTORY, emsg))

        config = configobj.ConfigObj(self.path)
        for key in DEFAULT_CONFIG.keys():
            if key in config:
                self[key] = config[key]


