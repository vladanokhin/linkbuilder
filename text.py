import os
import re
import frontmatter
from pathlib import Path
from config import Config
from typing import List, Tuple
from random import choice, randint, sample


class Text:

    listOfParagraphs: List[str] = []
    

    def __init__(self) -> None:
        self.config = Config()
        self.listOfPhrases = self.config.getValue('PHRASES_FOR_LINKS', ['More'])


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
        
        post = frontmatter.load(pathToSourcePost)
        listOfLinks = [f'[{title.title()}]({link})\n' for title, link in listOfLinksAndTitles]
        
        while listOfLinks:
            self.listOfParagraphs = re.split(r'\n(?=#)', post.content)
            statusPosition, randPosition = self.__getPostionForInsertLinks(pathToSourcePost)

            getCount = randint(1, len(listOfLinks))
            curentlistOfLinks = sample(listOfLinks, getCount)
            listOfLinks = [link for link in listOfLinks if not link in curentlistOfLinks]
            stringOfLinks = '\n'.join(curentlistOfLinks)

            if statusPosition == 'NotFound':
                randPhrase = choice(self.listOfPhrases)
                curentlistOfLinks.insert(0, f'### {randPhrase}:')
                stringOfLinks = '\n'.join(curentlistOfLinks)
                self.listOfParagraphs[randPosition] += '\n' + stringOfLinks + '\n'

            elif statusPosition == 'Before':
                self.listOfParagraphs[randPosition] = '\n' + stringOfLinks + '\n' + self.listOfParagraphs[randPosition]

            elif statusPosition == 'After':
                self.listOfParagraphs[randPosition] += '\n' + stringOfLinks + '\n'

            elif statusPosition == 'Warning':
                continue
            
            post.content = '\n'.join(self.listOfParagraphs)
        
        frontmatter.dump(post, pathToSourcePost)

        return True

    
    def __getPostionForInsertLinks(self, pathToSourcePost) -> Tuple[str, int]:
        lenOfList = len(self.listOfParagraphs)
        if lenOfList <= 1:
            return ('Warning', -1)
        
        randPosition = randint(1, lenOfList - 1)

        if randPosition + 1 > lenOfList - 1:
            randPosition -= 1

        
        prevHead, currentHead, nextHead = self.__getHeaderFromLines(
                                                        self.listOfParagraphs[randPosition - 1],
                                                        self.listOfParagraphs[randPosition],
                                                        self.listOfParagraphs[randPosition + 1]
                                                    )
        if prevHead in self.listOfPhrases and not\
           currentHead in self.listOfPhrases:
            return('Before', randPosition)

        elif currentHead in self.listOfPhrases:
            return('After', randPosition)

        elif currentHead not in self.listOfPhrases and \
             nextHead in self.listOfPhrases:
             return('After', randPosition + 1)
        elif currentHead not in self.listOfPhrases and \
             prevHead in self.listOfPhrases:
                return('Before', randPosition)
        elif (prevHead and currentHead and nextHead) not in self.listOfPhrases:
            return('NotFound', randPosition)
        else:
             return('Before', randPosition)
             



    def __getHeaderFromLines(self, *lines: str) -> List[str]:
        ressult = []
        if  lines:
            for line in lines:
                line = re.search(r'#*.*:$', line, re.MULTILINE)
                if line:
                    ressult.append(line.group(0)
                                        .replace('#', '')
                                        .replace(':', '')
                                        .strip()
                                )
                else:
                    ressult.append('')
        return ressult