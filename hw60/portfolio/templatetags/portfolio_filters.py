from django import template

register = template.Library()

@register.filter(name='replace_space')
def replace_space(value, arg):
    """
    Replaces all spaces in a string with the arg.
    For example: "Hello World" | replace_space:"_" -> "Hello_World"
    """
    if isinstance(value, str):
        return value.replace(' ', arg)
    return value
