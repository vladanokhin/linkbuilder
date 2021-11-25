import os
import re
import frontmatter
from pathlib import Path
from config import Config
from typing import List
from random import choice, randint


class Text:

    def __init__(self) -> None:
        self.config = Config()


    def getAllTextFromSite(self, site: str) -> List[str]:
        """
        Получить список всех постов с сайта
        :param site: название сайта
        :return список [{domain, filePath, content}] 
        """
        pathToSite = Path(self.config.getValue('path_to_sites', '/'), site)

        if not os.path.exists(Path(pathToSite, 'content')):
            raise FileNotFoundError(
                f'Not found {pathToSite}'
            )

        texts = []
        for filepath, dirs, files in os.walk(Path(pathToSite, 'content')):
            for file in files:
                if '_index.md' not in file:
                    pathToFile = str(Path(filepath,file))
                    post = frontmatter.load(pathToFile, encoding="ISO-8859-1")
                    if 'title' not in post:
                        continue

                    data = {
                        'domain': site,
                        'filePath': pathToFile,
                        'title': post['title'],
                        'content': re.sub(r'\!\[.*\]\(.*\)', '', post.content)
                                    .replace('#', '')
                                    .strip()
                    }

                    texts.append(data)
        
        return texts
    

    def writeLinksToPost(self, pathToSourcePost: str, 
                       listOfLinksAndTitles: List[str]) -> bool:
        """
        Вставляет в пост список ссылок на релевантные страници
        :param pathToSourcePost: путь к исходному посту, 
        в который будут вставлены ссылки
        :param listOfLinksAndTitles: список с тайтлами и ссылками на посты,
        которые будут вставлены в исходный пост
        """
        if not listOfLinksAndTitles or \
           not Path(pathToSourcePost).exists():
            return False
        
        randPhrase = self.__getRandomPhraseForLinks()
        post = frontmatter.load(pathToSourcePost)
        textPost = post.content
        listText = re.split(r'\n(?=#)', textPost)
        randPosition = choice(range(len(listText)))

        stringOfLinks = [f'[{title.title()}]({link})\n' for title, link in listOfLinksAndTitles]
        stringOfLinks.insert(0, '#' * randint(1,3) + f' {randPhrase}:')
        stringOfLinks = '\n'.join(stringOfLinks)
        listText[randPosition] += '\n' + stringOfLinks
        
        post.content = '\n'.join(listText)
        frontmatter.dump(post, pathToSourcePost)

        return True


    def __getRandomPhraseForLinks(self) -> str:
        """
        Возращет из конфига `(PHRASES_FOR_LINKS)` одну рандомную фразу для
        ссылок
        """
        listOfPhrases = self.config.getValue('phrases_for_links', ['More'])
        
        return choice(listOfPhrases)