
from .base import VMWareCommand


class ListCommand(VMWareCommand):
    name = 'list'
    short_description = 'List virtual machines'

    def run(self, args):
        args = self.parse_args(args)

        for virtualmachine in self.finder:
            self.message('{:20} {:32} {}'.format(
                virtualmachine.name,
                virtualmachine.uuid if virtualmachine.uuid is not None else '',
                virtualmachine.path
            ))
