from importlib import import_module

from django.apps import apps


def load(string, format='class'):

    allowed_formats = [
        'class',
        'string'
    ]

    if format not in allowed_formats:
        raise ValueError('Loader format not allowed')

    if format == 'string':
        return string

    parts = string.split('.')
    cls = parts.pop()
    module = import_module('.'.join(parts))

    return getattr(module, cls)


def get_model(string, format='class'):
    if format == 'string':
        return string
    parts = string.split('.')
    return apps.get_model(parts[0], parts[1])
