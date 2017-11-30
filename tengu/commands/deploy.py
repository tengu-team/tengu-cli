"""The deploy command."""


from json import dumps
from .base import Base


class Deploy(Base):

    def run(self):
        from sys import exit
        from subprocess import check_output, check_call, CalledProcessError, Popen
        self.ensure_deployable()
        try:
            check_call(['docker', 'build', '-t', self.options['--docker-repository'], self.options['--path']])
            check_call(['docker', 'push', self.options['--docker-repository']])
        except CalledProcessError as e:
            print(e)
            exit(1)
        self.create_k8s_configuration()
        self.deploy_to_k8s()

    def ensure_deployable(self):
        import os
        import sys
        if not os.path.exists(self.options['--path'] + '/Dockerfile'):
            print('No docker file found in ' + self.options['--path'])
            sys.exit(1)
        if not os.path.exists(self.options['--path'] + '/tengu'):
            os.makedirs(self.options['--path'] + '/tengu')

    def get_host_ip(self):
        from sys import exit
        from subprocess import check_output, CalledProcessError
        try:
            # Get default route ip
            return check_output(['ip', 'route', 'show']).decode('utf-8').rstrip().split()[2]
        except CalledProcessError as e:
            print(e)
            exit(1)

    def create_k8s_configuration(self):
        from datetime import datetime
        from tengu.utils import render
        render(source=self.package_dir + '/templates/deployment.tmpl',
               target=self.options['--path'] + '/tengu/kubernetes.yaml',
               context={'deploymentname': self.options['--workspace'],
                        'namespace': 'default',  # HARDCODED NAMESPACE !
                        'replicas': '1',
                        'selector': 'tengu',
                        'selectorname': self.options['--workspace'],
                        'rolling': 'true',
                        'containername': self.options['--workspace'],
                        'image': self.options['--docker-repository'],
                        'env_vars': {'deployedAt': datetime.now().isoformat()},
                        })

    def deploy_to_k8s(self):
        from sys import exit
        import os
        import json
        import yaml
        import requests
        url = 'http://' + self.get_host_ip() + ':5000/deploy/' + self.options['--workspace']
        headers = {'Content-Type': 'application/json'}
        try:
            with open(self.options['--path'] + '/tengu/kubernetes.yaml') as f:
                deployment = yaml.load(f)
                r = requests.put(url, data=json.dumps(deployment), headers=headers)
                if r.status_code == 200:
                    print("Deployment done")
        except OSError as e:
            print(e)
            exit(1)
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
