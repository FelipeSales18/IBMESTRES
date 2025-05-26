from django import template

register = template.Library()

@register.filter
def split(value, key):
    """Returns the value turned into a list split by key."""
    return value.split(key)

@register.filter
def trim(value):
    """Trims whitespace from a string."""
    return value.strip()