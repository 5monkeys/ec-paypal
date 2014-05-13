import logging
import re
from django.http import QueryDict  # TODO: Remove django dependency

DIGIT = re.compile('\d+')


def flatten_dict(dikt, branch=()):
    """
    Flatten dict of dicts|lists and yield (path-tuple, value).
    """
    for key, value in dikt.iteritems():
        path = branch + (key,)
        if isinstance(value, dict):
            for k, v in flatten_dict(value, path):
                yield k, v
        elif isinstance(value, list):
            for i, item in enumerate(value):
                for k, v in flatten_dict(item, path + (i,)):
                    yield k, v
        else:
            yield path, value


def collapse_dict(dikt, template, indices=()):
    """
    Collapse dict of dicts/lists and transform to flat dict with translated keys from template.
    """
    for key, value in dikt.iteritems():
        param = template.get(key)
        if not param:
            raise KeyError('Got invalid field %s' % key)
        if isinstance(value, dict):
            for k, v in collapse_dict(value, param, indices):
                yield k, v
        elif isinstance(value, list):
            for i, item in enumerate(value):
                for k, v in collapse_dict(item, param[0], indices + (i,)):
                    yield k, v
        else:
            yield param.format(*indices), value


def expand_dict(dikt, template):
    """
    Expand flat dict to dict of dicts/lists translated with template.
    """
    result = {}
    sorted_source = ((key, dikt[key]) for key in sorted(dikt.keys()))
    inverted_flat_mapping = {value.replace('{}', '0'): key for key, value in flatten_dict(template)}

    for key, value in sorted_source:
        indices = iter(map(int, DIGIT.findall(key)))
        pattern = DIGIT.sub('0', key)

        if not pattern in inverted_flat_mapping:
            logging.info('Got invalid field {}', key)
            continue

        nodes = iter(inverted_flat_mapping[pattern])
        node = next(nodes)
        leaf = result

        while True:
            ahead = next(nodes, None)
            if ahead is None:
                leaf[node] = value
                break

            if isinstance(ahead, int):
                array = leaf.get(node)
                if array is None:
                    array = leaf[node] = []
                try:
                    leaf = array[next(indices, 0)]
                except IndexError:
                    leaf = {}
                    array.append(leaf)
                ahead = next(nodes, None)
            else:
                next_leaf = leaf.get(node)
                if next_leaf is None:
                    leaf[node] = leaf = {}
                else:
                    leaf = next_leaf

            node = ahead  # next(nodes, 'X')

    return result


def querystring_to_dict(qs):
    """
    Convert query string parameters to dict.
    """
    return {param.upper(): value for param, value in QueryDict(qs).iteritems()}


def drop_empty_values(dikt):
    """
    Remove keys with value ''|None from dict.
    """
    for key, value in dikt.items():
        if not (unicode(value) if value is not None else None):
            del dikt[key]


def wrap_dicts_recursive(dikt, wrapper):
    """

    """
    def wrap(obj):
        if isinstance(obj, dict):
            obj = wrapper(obj)
            for key, value in obj.iteritems():
                obj[key] = wrap(value)
        elif isinstance(obj, (list, tuple)):
            for i in range(0, len(obj)):
                obj[i] = wrap(obj[i])
        return obj

    return wrap(dikt)


class DotDict(dict):
    """
    Dict with dot get|set access to keys.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__  # TODO: Not working properly
