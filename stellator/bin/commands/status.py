
from .base import VMWareCommand


class StatusCommand(VMWareCommand):
    name = 'status'
    short_description = 'Show VM status'

    def __register_arguments__(self, parser):
        parser.add_argument('patterns', nargs='*', help='VM name patterns to show')

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            self.message('{:20} {:9} {:3} CPUs {:5} MB memory {}'.format(
                virtualmachine.name,
                virtualmachine.status,
                virtualmachine.cores,
                virtualmachine.memory,
                'headless' if virtualmachine.headless else 'gui',
            ))
