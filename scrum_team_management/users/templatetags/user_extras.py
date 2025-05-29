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

@register.filter
def get_team_leader(assignments):
    return assignments.filter(role="Team Leader").first()