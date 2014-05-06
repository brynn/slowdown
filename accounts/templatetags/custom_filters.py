from django import template

register = template.Library()

@register.filter(name='hash')
def hash(h,key):
    if key in h:
        return h[key]
    else:
        return None