"""The base command."""


class Base(object):
    """A base command."""

    def __init__(self, options, package_dir, *args, **kwargs):
        self.options = options
        self.package_dir = package_dir
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')

    @staticmethod
    def get_host_ip():
        from sys import exit
        from subprocess import check_output, CalledProcessError
        try:
            # Get default route ip
            return check_output(['ip', 'route', 'show']).decode('utf-8').rstrip().split()[2]
        except CalledProcessError as e:
            print(e)
            exit(1)
