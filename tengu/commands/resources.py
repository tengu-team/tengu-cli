"""The resources command."""


from json import dumps
from .base import Base


class Resources(Base):

    def run(self):
        import requests
        from sys import exit
        url = 'http://' + self.get_host_ip() + ':5000/juju/applications'  # VERANDER NAAR /applications !!!!
        try:
            r = requests.get(url)
            print(json.dumps(r.json(), indent=2, sort_keys=True))
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
