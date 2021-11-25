from pathlib import Path
from typing import Union, Iterable
import random

class Config():

    # Названия модели
    TRANSFORMERS_MODEL = 'all-MiniLM-L6-v2'

    # Путь где лежать сайты
    PATH_TO_SITES = Path(Path.home(), 'Sites')  
    
    # Количество ссылок для добавления к исходной страници
    # Можно задавать в виде числа:
    # >>>  NUMBER_LINK_TO_ADD = 5
    # Или в виде диапазона, тогда будет добавлено
    # от 3 ссылок до 7, значения выбираеться рандомно:
    # >>> NUMBER_LINK_TO_ADD = (3,7)
    NUMBER_LINK_TO_ADD = (3,7)                

    # Путь приложения
    PROJECT_DIR = Path.cwd()
    
    # Фразы для подставки перед ссылками
    PHRASES_FOR_LINKS = [
        'Read More',
        'Also',
        'More',
        'More information',
        'Additional information'
    ]


    def getValue(self, name: str, default: Union[str, int, tuple] = None) -> Union[str, int, tuple]:
        """
        Возращает значени с конфига
        :param name: названия значения
        :param default: значения которое вернется, если искомого значения нету
        """
        lowerName = name.lower()
        upperName = name.upper()

        attrs = [str(attr).lower() for attr in dir(self) if not '__' in attr][:-1]

        if not lowerName in attrs:
            return default

        try:
            value = getattr(self, upperName)
            return value
        except AttributeError:
            return default