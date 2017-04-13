"""
Created on Thr Apr 13

@author: tzu-ting
"""

import json

__all__ = [
    'base_class',
    'quariable_class'
]

class base_class(dict):

    def __init__(self, name):
        self['name'] = name

    def __contains__(self, other) -> bool:
        if not hasattr(self, 'children'):
            return False
        for child in self.children:
            if child == other:
                return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self['name'] == other
        return super.__eq__(self, other)

    def __str__(self):
        return self.name

    def to_json(self):
        return json.dumps(self, indent = 4)

    @property
    def name(self):
        return self['name']

    @name.setter
    def name(self, name):
        self['name'] = name

    @property
    def id(self):
        return self.get('id', None)

    @id.setter
    def id(self, id):
        self['id'] = id

    @property
    def link(self):
        return self.get('link', None)

    @link.setter
    def link(self, id):
        self['link'] = id

    def append(self, obj):
        if not isinstance(obj, dict):
            raise TypeError()
        if not dict.__contains__(self, 'children'):
            dict.__setitem__(self, 'children', [])
        self['children'].append(obj)

class quariable_class(base_class):
    def query(self):
        raise RuntimeError()
