
from .base import VMWareCommand


class ListCommand(VMWareCommand):
    name = 'list'
    short_description = 'List virtual machines'

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in self.finder:
            self.message('{}'.format(virtualmachine.path))
