from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, ArithmeticError):
        return ''