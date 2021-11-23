import os
import re
import frontmatter
from pathlib import Path
from config import Config
from typing import Union, List


class Text:

    def __init__(self) -> None:
        self.config = Config()


    def getTextFromSite(self, site: str) -> Union[List[str], List[None]]:
        """
        Получить список всех постов с сайта
        :param site: название сайта
        :return список [{domain, filePath, content}] 
        """
        pathToSite = Path(self.config.getValue('pathToSites', '/'), site)

        if not os.path.exists(Path(pathToSite, 'content')):
            raise FileNotFoundError(
                f'Not found {pathToSite}'
            )

        texts = []
        for filepath, dirs, files in os.walk(Path(pathToSite, 'content')):
            for file in files:
                if '_index.md' not in file:
                    pathToFile = Path(filepath,file)
                    _frontmatter = frontmatter.load(pathToFile)
                    #TODO check
                    if 'title' not in _frontmatter:
                        continue

                    data = {
                        'domain': site,
                        'filePath': str(pathToFile),
                        # 'title': _frontmatter['title'],
                        'content': re.sub(r'\!\[.*\]\(.*\)', '', _frontmatter.content)
                                    .replace('#', '')
                                    .strip()
                    }

                    texts.append(data)
        
        return texts