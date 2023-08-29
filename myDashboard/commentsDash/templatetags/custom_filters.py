from __future__ import annotations

from django import template

register = template.Library()


@register.filter
def get_keys(dictionary):
    """
    A template filter that extracts keys from a dictionary and capitalizes them.

    Args:
        dictionary (dict): The dictionary from which keys are to be extracted.

    Returns:
        list: A list of capitalized keys from the dictionary.
    """
    keys = [key.capitalize() for key in dictionary.keys()]
    return keys


@register.filter
def get_values(dictionary):
    """
    A template filter that extracts values from a dictionary.

    Args:
        dictionary (dict): The dictionary from which values are to be extracted.

    Returns:
        list: A list of values from the dictionary.
    """
    values = [value for value in dictionary.values()]
    return values
