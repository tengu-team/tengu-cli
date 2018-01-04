"""The resources command."""


from json import dumps
from .base import Base


class Resources(Base):

    def run(self):
        import requests
        from sys import exit
        from tengu.utils import get_host_ip
        url = 'http://' + get_host_ip() + ':5000/juju/applications'
        try:
            r = requests.get(url)
            print(dumps(r.json(), indent=2, sort_keys=True))
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
