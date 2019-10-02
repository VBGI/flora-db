from django import template

register = template.Library()

try: 
    import markdown
except ImportError:
    markdown = None

def render_md(value):
    """Render a piece of text as HTML if it starts with MARKDOWN magic word"""

    if value.startswith('MARKDOWN:') and markdown:
        return markdown.markdown(value[9:])
    else:
        return value

register.filter('render_md', render_md)