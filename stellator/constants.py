"""
Constants for parsing vmware text configuration files
"""

# Generic config meta keys
CONFIG_META_KEYS = {
    '.encoding': 'encoding',
}

# Parsers for inventory
INVENTORY_VM_INTEGER_KEYS = (
    'ItemID',
    'ParentID',
    'SeqID',
)
INVENTORY_VM_BOOLEAN_FLAG_KEYS = (
    'IsCfgPathNormalized',
    'IsClone',
    'IsFavorite',
)
INVENTORY_VM_KEY_MAP = {
    'CfgVersion': 'configuration_version',
    'IsCfgPathNormalized': 'configuration_path_is_normalized',
    'IsClone': 'cloned',
    'IsFavorite': 'favorite',
    'ItemID': 'id',
    'ParentID': 'parent',
    'SeqID': 'sequence_id',
    'DisplayName': 'name',
    'UUID': 'uuid',
    'State': 'state',
}

# Constants for .vmx file parsing

VMX_INTEGER_KEYS = (
    'numvcpus',
    'memsize',
    'monitor.phys_bits_used',
    'svga.graphicsMemoryKB',
    'toolsInstallManager.updateCounter',
)
VMX_BOOLEAN_KEYS = (
    'cleanShutdown',
    'hpet0.present',
    'mem.hotadd',
    'mks.enable3d',
    'powerType.powerOff',
    'powerType.powerOn',
    'powerType.reset',
    'powerType.suspend',
    'replay.supported',
    'svga.guestBackedPrimaryAware',
    'softPowerOff',
    'vcpu.hotadd',
    'vmotion.checkpointFBSize',
    'vmotion.checkpointSVGAPrimarySize',
)
VMX_KEY_MAP = {
    'checkpoint.vmState': 'checkpoint_vmstate',
    'displayname': 'name',
    'displayName': 'name',
    'hpet0.present': 'hpet0_present',
    'memsize': 'memory',
    'numvcpus': 'cores',
    'nvram':  'nvram',
    'guestos': 'guest_os',
    'guestOS': 'guest_os',
    'gui.exitOnCLIHLT': 'gui_exit_on_client_halt',
    'gui.fullScreenAtPowerOn': 'gui_fullscreen_at_power_on',
    'gui.lastPoweredViewMode': 'gui_last_powered_view_mode',
    'gui.viewModeAtPowerOn': 'gui_view_mode_at_power_on',
    'cleanShutdown': 'clean_shutdown',
    'mem.hotadd': 'hotswap_mem',
    'migrate.hostlog': 'migrate_hostlog_filename',
    'mks.enable3d': 'enable_3d',
    'monitor.phys_bits_used': 'monitor_phys_bits_used',
    'replay.filename': 'replay_filename',
    'replay.supported': 'replay_supported',
    'vcpu.hotadd': 'hotswap_vcpu',
    'softPowerOff': 'soft_power_off',
    'powerType.powerOff': 'powertype_power_off',
    'powerType.powerOn': 'powertype_power_on',
    'powerType.reset': 'powertype_reset',
    'powerType.suspend': 'powertype_suspend',
    'extendedConfigFile': 'extended_config_file',
    'annotation': 'annotation',
    'config.version': 'compatibility_level',
    'svga.graphicsMemoryKB': 'svga_graphics_memory_kb',
    'svga.guestBackedPrimaryAware': 'svga_guestbacked_primate_aware',
    'tools.syncTime': 'tools_synctime',
    'tools.upgrade.policy': 'tools_upgrade_policy',
    'toolsInstallManager.updateCounter': 'tools_upgrade_counter',
    'uuid.bios': 'uuid_bios',
    'uuid.location': 'uuid_location',
    'virtualHW.version': 'virtual_hw_version',
    'virtualHW.productCompatibility': 'virtual_hw_product_compatibility',
    'vmotion.checkpointFBSize': 'vmotion_checkpoint_fb_size',
    'vmotion.checkpointSVGAPrimarySize': 'vmotion_checkpoint_svga_primary_size',
}

# Labels for fields to show in 'details' command
VMX_DETAILS_DESCRIPTIONS = (
    ( 'memory',               'Memory', ' MB', ),
    ( 'cores',                'CPUs', ),
    ( 'guest_os',             'Guest OS', ),
    ( 'enable_3d',            '3D Acceleration', ),
    ( 'compatibility_level',  'VM compatibility level', ),
    ( 'virtual_hw_version',   'VM virtual hardware version', ),
)

VMX_DEVICE_BOOLEAN_KEYS = (
    'present',
    'autodetect',
    'startConnected',
)
VMX_DEVICE_INTEGER_KEYS = (
    'pciSlotNumber',
)
VMX_DEVICE_KEY_MAP = {
    'deviceType': 'device_type',
    'fileName': 'filename',
    'startConnected': 'start_connected',
    'virtualDev': 'virtual_device',
}
