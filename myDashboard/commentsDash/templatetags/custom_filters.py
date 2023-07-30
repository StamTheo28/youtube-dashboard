from django import template

register = template.Library()



# Return a capitalised list of keys 
@register.filter
def get_keys(dictionary):
    keys = [key.capitalize() for key in dictionary.get_keys()]
    return keys

@register.filter
def get_values(dictionary):
    values = [value for value in dictionary.get_values()]
    return values