from django import template

register = template.Library()


@register.filter

def price_format(value):
    """Format a numeric price with a comma every three digits."""
    if value in (None, ""):
        return "0"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError, OverflowError):
        return value
