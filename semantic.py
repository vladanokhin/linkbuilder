from text import Text
from config import Config
from typing import List, Union
from sentence_transformers import SentenceTransformer, util


class SemanticSimilarity:

    scoreList: Union[List[int], List[None]] = []
    __isSortedList: bool = False
    __listOfPosts: List[str] = []


    def __init__(self, _text: Text) -> None:
        self.config = Config()
        self.model = SentenceTransformer(self.config.getValue('transformersModel'))
    

    def __sortListBySS(self, scoreList: List[int]) -> List[int]:
        """
        Сортирует массив по SS
        """
        return sorted(
            scoreList,
            key=lambda el: el[0],
            reverse=True
        )


    def textComparison(self, list: List[str]) -> Union[List[int], List[None]]:
        """
        Вычесляет SS для текстов и возращает отсортированный 
        список по SS
        """
        self.__listOfPosts = list
        self.scoreList = util.paraphrase_mining(self.model, [i['content'] for i in list])

        return self.getScoreList()


    def getScoreList(self) -> Union[List[int], List[None]]:
        """
        Возращает отсортированный список по SS
        """
        if self.scoreList is not None and not self.__isSortedList:
            self.scoreList = self.__sortListBySS(self.scoreList)
            self.__isSortedList = True

        return self.scoreList


    def getRelavantPages(self, id: int) -> Union[List[int], List[None]]:
        """
        Выбирает страницы с самым высоким SS среди других доменов
        :param id: индетификатор поста  
        """
        if not self.__listOfPosts:
            raise Exception(
                'List of posts not found. Before using this method you need compare text "textComparison()"'
            )

        countLinks = self.config.getValue('numberLinkToAdd', 5)
        currentDomain = self.__listOfPosts[id]['domain']
        listOfUsedDomains = []
        ressult = []
    
        # Выбираем все релевантные посты для исходного поста
        # Удаляем посты с текущего доменна 
        scoreList = list(filter(
            lambda post: self.__listOfPosts[post[2]]['domain'] != currentDomain,
            [post for post in self.getScoreList() if post[1] == id]
        ))

        # Выбираем по одному самому релевантному с домена
        for post in scoreList:
            relevantPostId = post[2]
            postData = self.__listOfPosts[relevantPostId]
            if postData['domain'] in listOfUsedDomains:
                continue

            ressult.append(post)
            listOfUsedDomains.append(postData['domain'])
            
        return self.__sortListBySS(ressult)[:countLinks]

    
    def getListOfPosts(self) -> Union[List[str], List[None]]:
        """
        Возращает ранее собранный список постов с сайтов
        """
        return self.__listOfPosts