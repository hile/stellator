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
    'cpuid.coresPerSocket',
    'monitor.phys_bits_used',
    'numa.autosize.cookie',
    'numa.autosize.vcpu.maxPerVirtualNode',
    'svga.graphicsMemoryKB',
    'toolsInstallManager.updateCounter',
    'toolsInstallManager.lastInstallError',
)
VMX_BOOLEAN_KEYS = (
    'acpi.smbiosVersion2.7',
    'chipset.useAcpiBattery',
    'chipset.useApmBattery',
    'cleanShutdown',
    'hgfs.linkRootShare',
    'hgfs.mapRootShare',
    'hpet0.present',
    'isolation.tools.hgfs.disable',
    'isolation.tools.copy.disable',
    'isolation.tools.dnd.disable',
    'isolation.tools.paste.disable',
    'mem.hotadd',
    'mks.enable3d',
    'powerType.powerOff',
    'powerType.powerOn',
    'powerType.reset',
    'powerType.suspend',
    'replay.supported',
    'svga.guestBackedPrimaryAware',
    'softPowerOff',
    'sound.autodetect',
    'sound.present',
    'vcpu.hotadd',
    'vpmc.enable',
    'vmotion.checkpointFBSize',
    'vmotion.checkpointSVGAPrimarySize',
    'vhv.enable',
)
VMX_KEY_MAP = {
    'acpi.smbiosVersion2.7': 'acpi_smbios_version_2.7',
    'bios.bootOrder': 'bios_boot_order',
    'bios.hddOrder': 'bios_hdd_order',
    'chipset.useAcpiBattery': 'chipset_use_acpi_battery',
    'chipset.useApmBattery': 'chipset_use_apm_battery',
    'cpuid.coresPerSocket': 'cpuid_cores_per_socket',
    'cleanShutdown': 'clean_shutdown',
    'checkpoint.vmState': 'checkpoint_vmstate',
    'displayname': 'name',
    'displayName': 'name',
    'hpet0.present': 'hpet0_present',
    'isolation.tools.hgfs.disable': 'isolation_tools_hgfs_disable',
    'isolation.tools.copy.disable': 'isolation_tools_copy_disable',
    'isolation.tools.dnd.disable': 'isolation_tools_dnd_disable',
    'isolation.tools.paste.disable': 'isolation_tools_paste_disable',
    'memsize': 'memory',
    'numvcpus': 'cores',
    'nvram':  'nvram',
    'guestos': 'guest_os',
    'guestOS': 'guest_os',
    'gui.exitOnCLIHLT': 'gui_exit_on_client_halt',
    'gui.fullScreenAtPowerOn': 'gui_fullscreen_at_power_on',
    'gui.lastPoweredViewMode': 'gui_last_powered_view_mode',
    'gui.viewModeAtPowerOn': 'gui_view_mode_at_power_on',
    'gui.perVMWindowAutofitMode': 'gui_per_vm_window_autofit_mode',
    'hgfs.linkRootShare': 'hgfs_link_root_share',
    'hgfs.mapRootShare': 'hgfs_map_root_share',
    'keyboardAndMouseProfile': 'keyboard_and_mouse_profile_id',
    'mem.hotadd': 'hotswap_mem',
    'migrate.hostlog': 'migrate_hostlog_filename',
    'mks.enable3d': 'enable_3d',
    'monitor.phys_bits_used': 'monitor_phys_bits_used',
    'numa.autosize.cookie': 'numa_autosize_cookie',
    'numa.autosize.vcpu.maxPerVirtualNode': 'numa_autosize_vcpu_max_per_virtual_node',
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
    'sound.autodetect': 'sound_autodetect',
    'sound.fileName': 'sound_filename',
    'sound.pciSlotNumber': 'sound_pci_slot_number',
    'sound.present': 'sound_present',
    'tools.syncTime': 'tools_synctime',
    'tools.upgrade.policy': 'tools_upgrade_policy',
    'toolsInstallManager.updateCounter': 'tools_upgrade_counter',
    'toolsInstallManager.lastInstallError': 'tools_manager_last_install_error',
    'uuid.bios': 'uuid_bios',
    'uuid.location': 'uuid_location',
    'virtualHW.version': 'virtual_hw_version',
    'virtualHW.productCompatibility': 'virtual_hw_product_compatibility',
    'vmotion.checkpointFBSize': 'vmotion_checkpoint_fb_size',
    'vmotion.checkpointSVGAPrimarySize': 'vmotion_checkpoint_svga_primary_size',
    'vpmc.enable': 'vpmc_enable',
    'virtualhw.version': 'virtual_hw_version',
    'vhv.enable': 'virtual_hypervisor_enable',
}

# Labels for fields to show in 'details' command
VMX_DETAILS_DESCRIPTIONS = (
    ('uuid',                       'UUID'),
    ('memory',                     'Memory', ' MB',),
    ('cores',                      'CPUs',),
    ('guest_os',                   'Guest OS',),
    ('enable_3d',                  '3D Acceleration',),
    ('sound_present',              'Soundcard present',),
    ('virtual_hypervisor_enable',  'Nested Virtualization'),
    ('compatibility_level',        'VM compatibility level',),
    ('virtual_hw_version',         'VM virtual hardware version',),
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
