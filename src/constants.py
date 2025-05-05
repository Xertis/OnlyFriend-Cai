import os
from dotenv import load_dotenv

load_dotenv('ваш файл .env')

# TODO: Расскоментировать, когда будет создан класс Structure и доделан Constants


class Meta(type):
    def __getitem__(self, key):
        # Позволяет получать значения по ключу, как в словаре.
        if key == "TOKEN":
            return self.TOKEN
        elif key == "NN_MODEL":
            return self.NN_MODEL
        else:
            raise KeyError(f"'{key}' не найдено")


class Structure:
    def __init__(self):
        self._values = {
            'TOKEN': os.getenv('TOKEN'),
            'NN_MODEL': os.getenv('NN_MODEL')
        }

    def get(self, key):
        # Возвращает значение по ключу.
        return self._values.get(key)

    def set(self, key, value):
        # Устанавливает значение по ключу.
        self._values[key] = value


class Constants(metaclass=Meta):
    TOKEN = Structure().get('TOKEN')
    NN_MODEL = Structure().get('NN_MODEL0')
    _immutable_attributes = ['_TOKEN', '_NN_MODEL']

    def __init__(self):
        self.structure = Structure()
        self._TOKEN = self.structure.get('TOKEN')
        self._NN_MODEL = self.structure.get('NN_MODEL')

    def __setattr__(self, key, value):
        # Запрещаем изменение существующих неизменяемых атрибутов
        if key in self._immutable_attributes:
            raise AttributeError(f"Нельзя изменить значение атрибута '{key}'")
        super().__setattr__(key, value)

    def get_token(self):
        # Возвращает переменную окружения TOKEN.
        return self._TOKEN

    def get_nn_model(self):
        # Возвращает переменную окружения NN_MODEL.
        return self._NN_MODEL

    def set_token(self, value):
        # Устанавливает новое значение для TOKEN в структуре.
        self.structure.set('TOKEN', value)

    def set_nn_model(self, value):
        # Устанавливает новое значение для NN_MODEL в структуре.
        self.structure.set('NN_MODEL', value)


for key, val in os.environ.items():
    setattr(Constants, key, val)