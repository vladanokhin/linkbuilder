import re
import os
from typing import Dict, List, Set
from subprocess import check_output
from pathlib import Path
from config import Config


class Hugo:

    __sitesPostsList: dict = {}

    def __init__(self) -> None:
        self.config = Config()
        self.pathToSites = self.config.getValue('path_to_sites')


    def getPostPermaLink(self, domain: str, pathToPost: str) -> str:
        """
        Возращает web-ссылку на пост, по локальноку пути на пост
        :param domain: название сайта
        :param pathToPost: путь к посту в файловой системе
        """
        if not domain in self.__sitesPostsList.keys():
            self.__parseDomainLinks(domain)

        return self.__sitesPostsList[domain][pathToPost]   


    def __parseDomainLinks(self, domain: str) -> bool:
        """
        Парсит и сохраняет все web-ссылки сайта
        :param domain: название сайта
        """
        pathToSite = Path(self.pathToSites, domain)
        self.__sitesPostsList.update({domain: {}})

        if not Path(pathToSite).exists():
            return False

        os.chdir(pathToSite)
        _resText = check_output(['hugo', 'list', 'all']).decode('utf-8')
        
        for line in _resText.split('\n')[1:]:
            line = list(filter(None, line.split(',')))
            if not line:
                continue

            pathToPost = str(Path(pathToSite, line[0]))
            url = list(filter(lambda x: re.match(r'https?://(\w*||\S*)*/', x), 
                              line[1:]))

            self.__sitesPostsList[domain][pathToPost] = url[0]

        os.chdir(self.config.getValue('project_dir'))
        return True