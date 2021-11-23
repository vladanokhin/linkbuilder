from text import Text
from config import Config
from typing import List, Union
from sentence_transformers import SentenceTransformer, util


class SemanticSimilarity:

    scoreList: Union[List[int], List[None]] = []
    isSortedList: bool = False

    def __init__(self, _text: Text) -> None:
        self.config = Config()
        self.model = SentenceTransformer(self.config.getValue('transformersModel'))
        self._textSites = _text
    
    
    def textComparison(self, list: List[str]) -> Union[List[int], List[None]]:
        """
        Вычесляет SS для текстов и возращает отсортированный 
        список по SS
        """
        self.scoreList = util.paraphrase_mining(self.model, [i['content'] for i in list])

        return self.getScoreList()


    def getScoreList(self) -> Union[List[int], List[None]]:
        """
        Возращает отсортированный список по SS
        """
        if self.scoreList is not None and not self.isSortedList:
            self.scoreList = sorted(
                self.scoreList, 
                key=lambda el: el[0],
                reverse=True
            )
            self.isSortedList = True

        return self.scoreList


    def getRelavantPages(self, id: int) -> Union[List[int], List[None]]:
        """
        Выбирает страницы с самым высоким SS среди других доменов
        :param id: индетификатор поста
        """
        countLinks = self.config.getValue('numberLinkToAdd', 5)

        scoreList = [el for el in self.getScoreList() if el[1] == id]
        
        return scoreList[:countLinks]


