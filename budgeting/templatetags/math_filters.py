# budgeting/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def mul(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0