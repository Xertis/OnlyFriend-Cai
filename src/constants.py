import os
from os import environ

from dotenv import load_dotenv

load_dotenv()

# TODO: Расскоментировать, когда будет создан класс Structure и доделан
# Constants


class Struct:
    def __init__(self, *args, **kwargs):

        self._data = {}
        self._keys_order = []

        for idx, value in enumerate(args):
            key = str(idx)
            self._data[key] = value
            self._keys_order.append(key)

        for key, value in kwargs.items():
            self._data[key] = value
            self._keys_order.append(key)

    def __getitem__(self, key):

        if isinstance(key, int):
            key = str(key)
            return self._data.get(key, None)
        return self._data.get(key, None)

    def __setitem__(self, key, value):

        if isinstance(key, int):
            key = str(key)
        if key not in self._data:
            self._keys_order.append(key)
        self._data[key] = value

    def __getattr__(self, name):

        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'Struct' object has no attribute '{name}'")

    def __setattr__(self, name, value):

        if name in ('_data', '_keys_order'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            if name not in self._keys_order:
                self._keys_order.append(name)

    def __len__(self):

        return len(self._data)

    def __iter__(self):

        return iter(self._keys_order)

    def __str__(self):

        items = [f"{key}: {self._data[key]}" for key in self._keys_order]
        return "{" + ", ".join(items) + "}"

    def __repr__(self):

        return self.__str__()