#!/usr/bin/env python

from systematic.shell import Script

from ..config import DEFAULT_CONFIG_PATH
from .commands.list import ListCommand
from .commands.details import DetailsCommand
from .commands.start import StartCommand
from .commands.stop import StopCommand
from .commands.resume import ResumeCommand
from .commands.status import StatusCommand
from .commands.suspend import SuspendCommand


def main():
    script = Script()
    script.add_argument('--config', default=DEFAULT_CONFIG_PATH, help='Virtual machine directory')

    script.add_subcommand(ListCommand())
    script.add_subcommand(StatusCommand())
    script.add_subcommand(StartCommand())
    script.add_subcommand(StopCommand())
    script.add_subcommand(ResumeCommand())
    script.add_subcommand(SuspendCommand())
    script.add_subcommand(DetailsCommand())

    script.parse_args()


if __name__ == '__main__':
    main()
