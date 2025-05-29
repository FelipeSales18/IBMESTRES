from django import template

register = template.Library()

@register.filter
def has_external_po(assignments):
    return assignments.filter(role="External PO").exists()

@register.filter
def get_external_po(assignments):
    return assignments.filter(role="External PO").first()