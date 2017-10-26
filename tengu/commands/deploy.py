"""The deploy command."""


from json import dumps
from .base import Base


class Deploy(Base):

    def run(self):
        from subprocess import check_output, check_call, CalledProcessError, Popen
        # print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        self.ensure_deployable()
        pod = self.get_k8s_pod()
        kube_proxy = Popen(['kubectl', 'port-forward', '-n', 'kube-system', pod, '5000:5000'])
        try:
            check_call(['docker', 'build', '-t', self.options['--workspace'], self.options['--path']])
            check_call(['docker', 'tag', self.options['--workspace'],
                        'localhost:5000/tengu/'+ self.options['--workspace']])
            check_call(['docker', 'push', 'localhost:5000/tengu/' + self.options['--workspace']])
        except CalledProcessError as e:
            print(e)
        kube_proxy.terminate()
        self.create_k8s_configuration()

    def ensure_deployable(self):
        import os
        import sys
        if not os.path.exists(self.options['--path'] + '/Dockerfile'):
            print('No docker file found in ' + self.options['--path'])
            sys.exit(1)
        if not os.path.exists(self.options['--path'] + '/tengu'):
            os.makedirs(self.options['--path'] + '/tengu')

    def get_k8s_pod(self):
        from subprocess import check_output, CalledProcessError
        from sys import exit

        cmd = ['kubectl', 'get', 'pods', '-n', 'kube-system', '-l', 'k8s-app=kube-registry-upstream',
               '-o', 'template', '--template',
               "'{{range .items}}{{.metadata.name}} {{.status.phase}}{{\"\\n\"}}{{end}}'"]
        try:
            pods = check_output(cmd).decode('utf-8')
        except CalledProcessError as e:
            print(e)
            exit(1)
        return pods.split()[0].lstrip("'")

    def create_k8s_configuration(self):
        from datetime import datetime
        from tengu.utils import render
        render(source=self.package_dir + '/templates/deployment.tmpl',
               target=self.options['--path'] + '/tengu/kubernetes.yaml',
               context={'deploymentname': self.options['--workspace'],
                        'namespace': 'dev',  # HARDCODED NAMESPACE !
                        'replicas': '1',
                        'selector': 'tengu',
                        'selectorname': self.options['--workspace'],
                        'rolling': 'true',
                        'containername': self.options['--workspace'],
                        'image': 'localhost:5000/tengu/'+ self.options['--workspace'],
                        'env_vars': ['deployedAt=' + datetime.now().isoformat()],
                        })
