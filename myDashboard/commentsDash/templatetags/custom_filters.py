from django import template

register = template.Library()


@register.filter
def get_values(dictionary):
    return list(dictionary.values())


# Return a capitalised list of keys 
@register.filter
def get_paginator_emotion_keys(page):
    keys = [key.capitalize() for key in page[0]]
    return keys