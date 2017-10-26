def render(source, context, target):
    import os
    import jinja2
    path, filename = os.path.split(source)
    with open(target, 'w+') as f:
        f.write(jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context))