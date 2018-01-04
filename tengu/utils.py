def render(source, context, target):
    import os
    import jinja2
    path, filename = os.path.split(source)
    with open(target, 'w+') as f:
        f.write(jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context))


def get_host_ip():
    from sys import exit
    from subprocess import check_output, CalledProcessError
    try:
        # Get default route ip
        return check_output(['ip', 'route', 'show']).decode('utf-8').rstrip().split()[2]
    except CalledProcessError as e:
        print(e)
        exit(1)
