import os
from dotenv import load_dotenv

load_dotenv('TOKEN.env')


class Meta(type):
    def __getitem__(cls, key):
        if key == "TOKEN":
            return cls._TOKEN
        elif key == "NN_MODEL":
            return cls._NN_MODEL
        else:
            raise KeyError(f"'{key}' не найдено")


class Constants(metaclass=Meta):
    _TOKEN = os.getenv('TOKEN')
    _NN_MODEL = os.getenv('NN_MODEL')

    @classmethod
    def get_token(cls):
        return cls._TOKEN


    @classmethod
    def get_nn_model(cls):
        return cls._NN_MODEL


for key, val in os.environ.items():
    setattr(Constants, key, val)
