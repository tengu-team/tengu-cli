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
