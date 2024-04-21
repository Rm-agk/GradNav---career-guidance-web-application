from django import template

register = template.Library()

@register.filter
def remove_hyphens(value):
    """Removes all hyphens from a string or each string in a list."""
    if isinstance(value, list):
        return [item.replace('/n-', '') for item in value]
    return value.replace('-', '')
