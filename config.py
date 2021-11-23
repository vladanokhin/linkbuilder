from pathlib import Path
from typing import Union

class Config():
    
    values = {
        'transformersModel': 'all-MiniLM-L6-v2',    # Названия модели
        'pathToSites': Path(Path.home(), 'Sites'),  # Путь где лежать сайты
        'numberLinkToAdd': 5                        # Количество ссылок для добавления к исходной страници
    }

    def getValue(self, name: str, default: Union[str, int, None] = None) -> Union[str, int, None]:
        """
        Возращает значени с конфига
        :param name: названия значения
        """
        return self.values[name] if name in self.values.keys() else default