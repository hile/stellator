
from .base import VMWareCommand


class ResumeCommand(VMWareCommand):
    name = 'resume'
    short_description = 'Resume virtual machines'

    def __register_arguments__(self, parser):
        parser.add_argument('patterns', nargs='*', help='VM name patterns to resume')

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in args.virtualmachines:
            if not virtualmachine.headless or not virtualmachine.autoresume:
                continue

            if not self.finder.is_running(virtualmachine):
                self.message('resume {}'.format(virtualmachine))
                virtualmachine.start()
