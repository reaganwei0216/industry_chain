# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 23:22:46 2017

@author: tzu-ting
"""

def to_str(key):
    if isinstance(key, str):
        return key

    elif isinstance(key, tuple) and len(key)==2:
        msg = f'{key[0]}'
        for sub_item in key[1]:
            msg += f'\n\t{sub_item}'
        return msg

    elif hasattr(key, '__iter__'):
        return '\n'.join([to_str(s) for s in key])

    else:
        return super.__str__(key)

class base_class:

    @property
    def keys(self) -> list:
        return self.get_key()

    @property
    def details(self) -> list:
        return self.get_detail()

    def get_key(self) -> list:
        pass

    def get_detail(self) -> list:
        pass

    def __contains__(self, obj):
        return obj in self.keys

    def __str__(self):
        return to_str(self.keys)
