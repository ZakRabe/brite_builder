from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def champLink(value):
    """Converts a string into all lowercase and replaces spaces with hyphens"""
    return value.lower().replace(" ", "-").replace("'", '')

@register.filter
@stringfilter
def champName(value):
    """Converts a champLink to a champion name to match against a model title"""
    title = value.replace('-', ' ')
    return " ".join(w.capitalize() for w in title.split())

@register.filter
@stringfilter
def ng(value):
    """wraps angular expressions"""
    return '{{' + value + "}}"