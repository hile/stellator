
from .base import VMWareCommand


class StopCommand(VMWareCommand):
    name = 'stop'
    short_description = 'Stop virtualmachines'

    def __register_arguments__(self, parser):
        parser.add_argument('patterns', nargs='*', help='VM name patterns to stop')

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if self.finder.is_running(virtualmachine):
                self.message('stop {}'.format(virtualmachine))
                virtualmachine.stop()
