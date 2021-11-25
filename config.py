from pathlib import Path
from typing import Union, Iterable

class Config():
    
    TRANSFORMERS_MODEL = 'all-MiniLM-L6-v2'     # Названия модели

    PATH_TO_SITES = Path(Path.home(), 'Sites')  # Путь где лежать сайты

    NUMBER_LINK_TO_ADD = 3                      # Количество ссылок для добавления к исходной страници

    PROJECT_DIR = Path.cwd()
    
    PHRASES_FOR_LINKS = [
        'Read More',
        'Also',
        'More',
        'More information',
        'Additional information',
    ]

    def getValue(self, name: str, default: Union[str, int, None] = None) -> Union[str, int, None]:
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