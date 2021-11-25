from text import Text
from config import Config
from typing import List, Union
from sentence_transformers import SentenceTransformer, util


class SemanticSimilarity:

    scoreList: List[int] = []
    __isSortedList: bool = False
    __listOfPosts: List[str] = []


    def __init__(self) -> None:
        self.config = Config()
        self.model = SentenceTransformer(self.config.getValue('TRANSFORMERS_MODEL'))
    

    def __sortListBySS(self, scoreList: List[int]) -> List[int]:
        """
        Сортирует массив по SS
        :param scoreList: список с данными сравнений текстов
        """
        return sorted(
            scoreList,
            key=lambda el: el[0],
            reverse=True
        )


    def textComparison(self, list: List[str]) -> List[int]:
        """
        Вычесляет SS для текстов и возращает отсортированный 
        список по SS
        :param list: список с текстами
        """
        self.__listOfPosts = list
        self.scoreList = util.paraphrase_mining(self.model, [i['content'] for i in list])

        return self.getScoreList()


    def getScoreList(self) -> List[int]:
        """
        Возращает отсортированный список по SS
        """
        if self.scoreList is not None and not self.__isSortedList:
            self.scoreList = self.__sortListBySS(self.scoreList)
            self.__isSortedList = True

        return self.scoreList


    def getRelavantPages(self, id: int) -> List[int]:
        """
        Выбирает страницы с самым высоким SS среди других доменов
        :param id: индетификатор поста  
        """
        if not self.__listOfPosts:
            raise Exception(
                'List of posts not found. Before using this method you need compare text "textComparison()"'
            )

        countLinks = self.config.getValue('number_link_to_add', 5)
        currentDomain = self.__listOfPosts[id]['domain']
        listOfUsedDomains = []
        ressult = []
    
        # Выбираем все релевантные посты для исходного поста
        # Удаляем посты с текущего доменна 
        scoreList = list(filter(
            lambda post: self.__listOfPosts[post[2]]['domain'] != currentDomain,
            [post for post in self.getScoreList() if post[1] == id]
        ))

        # Выбираем по одному самому релевантному тексту с домена
        for post in scoreList:
            relevantPostId = post[2]
            postData = self.__listOfPosts[relevantPostId]
            if postData['domain'] in listOfUsedDomains:
                continue

            ressult.append(post)
            listOfUsedDomains.append(postData['domain'])

        return self.__sortListBySS(ressult)[:countLinks]