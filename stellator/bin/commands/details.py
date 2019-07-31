
from .base import VMWareCommand
from ...constants import VMX_DETAILS_DESCRIPTIONS


class DetailsCommand(VMWareCommand):
    name = 'details'
    short_description = 'Show VM details'

    def __register_arguments__(self, parser):
        parser.add_argument('patterns', nargs='*', help='VM name patterns to stop')

    def run(self, args):
        args = self.parse_args(args)

        # Add empty before first VM
        self.message('')

        for virtualmachine in args.virtualmachines:
            self.message('{}'.format(virtualmachine.name))
            for detail in VMX_DETAILS_DESCRIPTIONS:
                label = detail[1]
                value = getattr(virtualmachine, detail[0])
                units = len(detail) > 2 and detail[2] or ''
                if isinstance(value, bool):
                    value = value is True and 'Enabled' or 'Disabled'
                if value is None:
                    value = 'not available'
                self.message('  {:30} {}{}'.format(label, value, units))

            self.message('\n  Network Interfaces')
            for interface in virtualmachine.interfaces:
                ipaddress = interface.ip_address
                connection_type = getattr(interface, 'connection_type', None)
                self.message('    {} {:11} {:8} {:8} {:10} {} {}'.format(
                    interface.index,
                    'autoconnect' if interface.autoconnect is True else 'manual',
                    connection_type if connection_type is not None else 'unknown',
                    interface.driver,
                    interface.address_type,
                    interface.mac_address,
                    ipaddress if ipaddress is not None else '',
                ))

            if virtualmachine.shared_folders.shares:
                self.message('\n  Shared Folders')
                for share in virtualmachine.shared_folders.shares:
                    self.message('    {:12} {:8} {:8} {}'.format(
                        share.guest_folder_name,
                        'enabled' if share.enabled else 'disabled',
                        'writable' if share.guest_write_access else '',
                        share.host_path,
                    ))

            if virtualmachine.description:
                description = '\n  '.join(virtualmachine.description.splitlines())
                self.message('\n  Description:\n\n  {}'.format(description))

            # Add empty line between VMs
            self.message('')
