"""
Created on Thr Apr 13

@author: tzu-ting
"""

import json

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
        return json.dumps(
            self,
            indent = 4,
            ensure_ascii = False
        )

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

    @property
    def children(self) -> list:
        if not dict.__contains__(self, 'children'):
            dict.__setitem__(self, 'children', [])
        return self.get('children')

    def append(self, obj):
        if not isinstance(obj, dict):
            raise TypeError()
        self.children.append(obj)

    def query(self):
        raise RuntimeError('query func not implemented')
