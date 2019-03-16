#!/usr/bin/env python

from systematic.shell import Script, ScriptCommand

from stellator.config import StellatorConfig, DEFAULT_CONFIG_PATH
from stellator.constants import VMX_DETAILS_DESCRIPTIONS
from stellator.inventory import VirtualMachineFinder


class VMWareCommand(ScriptCommand):
    def parse_args(self, args):
        self.config = StellatorConfig(args.config)
        self.finder = VirtualMachineFinder(self.config)

        if 'patterns' in args:
            if args.patterns:
                args.virtualmachines = self.finder.match_vm_names(
                    [pattern for arg in args.patterns for pattern in arg.split(',')]
                )
            else:
                args.virtualmachines = [vm for vm in self.finder]

        return args


class ListCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in self.finder:
            self.message('{0}'.format(virtualmachine.path))


class StartCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if not self.finder.is_running(virtualmachine):
                self.message('start {0}'.format(virtualmachine))
                virtualmachine.start()


class AutoResumeCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if not virtualmachine.headless or not virtualmachine.autoresume:
                continue

            if not self.finder.is_running(virtualmachine):
                self.message('resume {0}'.format(virtualmachine))
                virtualmachine.start()


class StopCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if self.finder.is_running(virtualmachine):
                self.message('stop {0}'.format(virtualmachine))
                virtualmachine.stop()


class SuspendCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        if not args.patterns and args.autoresume:
            args.virtualmachines = [vm for vm in args.virtualmachines if vm.headless]

        for virtualmachine in args.virtualmachines:
            if self.finder.is_running(virtualmachine):
                self.message('suspend {0}'.format(virtualmachine))
                virtualmachine.suspend(autoresume=args.autoresume)


class StatusCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            self.message('{0:12} {1:9} {2:3} CPUs {3:5} MB memory {4}'.format(
                virtualmachine.name,
                virtualmachine.status,
                virtualmachine.cores,
                virtualmachine.memory,
                virtualmachine.headless and 'headless' or 'gui',
            ))


class DetailsCommand(VMWareCommand):
    def run(self, args):
        args = self.parse_args(args)

        # Add empty before first VM
        self.message('')

        for virtualmachine in args.virtualmachines:
            self.message('{0}'.format(virtualmachine.name))
            for detail in VMX_DETAILS_DESCRIPTIONS:
                label = detail[1]
                value = getattr(virtualmachine, detail[0])
                units = len(detail) > 2 and detail[2] or ''
                if isinstance(value, bool):
                    value = value is True and 'Enabled' or 'Disabled'
                if value is None:
                    value = 'not available'
                self.message('  {0:30} {1}{2}'.format(label, value, units))

            self.message('\n  Network Interfaces')
            for interface in virtualmachine.interfaces:
                ipaddress = interface.ip_address
                self.message('    {0} {1:11} {2:8} {3:8} {4:10} {5} {6}'.format(
                    interface.index,
                    interface.autoconnect is True and 'autoconnect' or 'manual',
                    interface.connection_type,
                    interface.driver,
                    interface.address_type,
                    interface.mac_address,
                    ipaddress is not None and ipaddress or '',
                ))

            if virtualmachine.shared_folders.shares:
                self.message('\n  Shared Folders')
                for share in virtualmachine.shared_folders.shares:
                    self.message('    {0:12} {1:8} {2:8} {3}'.format(
                        share.guest_folder_name,
                        share.enabled and 'enabled' or 'disabled',
                        share.guest_write_access and 'writable' or '',
                        share.host_path,
                    ))

            if virtualmachine.description:
                description = '\n  '.join(virtualmachine.description.splitlines())
                self.message('\n  Description:\n\n  {0}'.format(description))

            # Add empty line between VMs
            self.message('')


def main():
    script = Script()
    script.add_argument('--config', default=DEFAULT_CONFIG_PATH, help='Virtual machine directory')

    c = script.add_subcommand(ListCommand('list', 'List VMs'))

    c = script.add_subcommand(StartCommand('start', 'Start VM'))
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    c = script.add_subcommand(StopCommand('stop', 'Stop VM'))
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    c = script.add_subcommand(AutoResumeCommand('resume', 'Autoresume headless VMs'))
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    c = script.add_subcommand(SuspendCommand('suspend', 'Suspend VM'))
    c.add_argument('--autoresume', action='store_true', help='Set autoresume flag')
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    c = script.add_subcommand(StatusCommand('status', 'Show status of VMs'))
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    c = script.add_subcommand(DetailsCommand('details', 'Show VM details'))
    c.add_argument('patterns', nargs='*', help='VM name patterns')

    script.parse_args()


if __name__ == '__main__':
    main()
