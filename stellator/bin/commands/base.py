
from systematic.shell import ScriptCommand
from stellator.config import StellatorConfig
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
