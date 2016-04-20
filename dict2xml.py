"""Converts a dictionary into an XML document"""

import collections

from lxml import etree


def build(dictionary, root=None):
    if root is None:
        root = 'root'

    element = _build_element_from_dict(root, dictionary)

    return etree.tostring(element)


def _build_element_from_dict(name, dictionary, parent_namespace=None):
    try:
        namespace = dictionary['#ns']
    except KeyError:
        namespace = parent_namespace

    tag = _make_tag(name, namespace)
    element = etree.Element(tag)

    for key, value in dictionary.iteritems():
        if key == '#ns':
            pass
        elif key.startswith('@'):
            element.set(key[1:], value)
        elif key == '#text':
            element.text = _convert_to_text(value)
        else:
            _add_sub_elements(element, key, value, namespace)

    return element


def _make_tag(name, namespace):
    if namespace is None:
        tag = name
    else:
        tag = etree.QName(namespace, name)

    return tag


def _add_sub_elements(element, name, value, namespace):
    if isinstance(value, collections.Mapping):
        element.append(_build_element_from_dict(name, value, namespace))
    elif (isinstance(value, collections.Iterable) and
          not isinstance(value, basestring)):
        for sub_elem in _build_elements_from_list(name, value, namespace):
            element.append(sub_elem)
    else:
        element.append(_build_element_from_value(name, value, namespace))


def _build_elements_from_list(name, list_, parent_namespace):
    for item in list_:
        if isinstance(item, collections.Mapping):
            element = _build_element_from_dict(name, item, parent_namespace)
        else:
            element = _build_element_from_value(name, item, parent_namespace)

        yield element


def _build_element_from_value(name, value, parent_namespace):
    tag = _make_tag(name, parent_namespace)
    element = etree.Element(tag)
    element.text = _convert_to_text(value)
    return element


def _convert_to_text(value):
    if value is None:
        text = None
    elif isinstance(value, bool):
        text = 'true' if value else 'false'
    else:
        text = str(value)

    return text