
from .base import VMWareCommand


class StartCommand(VMWareCommand):
    name = 'start'
    short_description = 'Stop virtualmachines'

    def __register_arguments__(self, parser):
        parser.add_argument('--headless', action='store_true', help='Start VMs in headless mode')
        parser.add_argument('patterns', nargs='*', help='VM name patterns to start')

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if not self.finder.is_running(virtualmachine):
                self.message('start {}'.format(virtualmachine))
                virtualmachine.start(headless=args.headless)
