
from .base import VMWareCommand


class SuspendCommand(VMWareCommand):
    name = 'suspend'
    short_description = 'Suspend VM'

    def __register_arguments__(self, parser):
        parser.add_argument('--autoresume', action='store_true', help='Set autoresume flag')
        parser.add_argument('patterns', nargs='*', help='VM name patterns to suspend')

    def run(self, args):
        args = self.parse_args(args)

        if not args.patterns and args.autoresume:
            args.virtualmachines = [vm for vm in args.virtualmachines if vm.headless]

        for virtualmachine in args.virtualmachines:
            if self.finder.is_running(virtualmachine):
                self.message('suspend {}'.format(virtualmachine))
                virtualmachine.suspend(autoresume=args.autoresume)
