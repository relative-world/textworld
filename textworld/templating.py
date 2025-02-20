from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("textworld"), autoescape=select_autoescape())


def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)
