"""
tengu
Usage:
  tengu hello
  tengu deploy (--path=<path>) (--workspace=<workspace>) (--namespace=<namespace>) (--docker-repository=<dockerrepo>)
  tengu -h | --help
  tengu --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
Examples:
  tengu hello
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tengu-team/tengu-cli
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import tengu.commands
    import os
    options = docopt(__doc__, version=VERSION)
    package_directory = os.path.dirname(os.path.abspath(__file__))

    for (k, v) in options.items():
        if hasattr(tengu.commands, k) and v:
            module = getattr(tengu.commands, k)
            tengu.commands = getmembers(module, isclass)
            command = [command[1] for command in tengu.commands if command[0] != 'Base'][0]
            command = command(options, package_directory)
            command.run()
