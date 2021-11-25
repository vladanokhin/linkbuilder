import json
import argparse
import os
from hugo import Hugo
from text import Text
from pathlib import Path
from semantic import SemanticSimilarity
from tqdm import tqdm
from tabulate import tabulate


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', type=str, required=True,
        help="Путь к списку с доменами, обезательный. (path/to/list.txt)"
    )     

    return parser


def main():
    textSites = Text()
    semanticSimilarity = SemanticSimilarity()
    hugo = Hugo()

    with open(path_to_list) as f:
        lines = f.readlines()
    
    # Собираем текста со всех сайтов
    listOfTexts = list()
    for line in lines:
        site = line.strip()
        textFromSite = textSites.getAllTextFromSite(site)
        if textFromSite:
            listOfTexts.extend(textFromSite)

    # Сематическое сравнение текстов между собой
    semanticSimilarity.textComparison(listOfTexts)
    ressultData = {}
    for id in range(0, len(listOfTexts)):
        scoreList = semanticSimilarity.getRelavantPages(id)
        if not scoreList:
            continue
    
        sourcePostData = listOfTexts[id]
        if not sourcePostData['domain'] in ressultData.keys():
            ressultData[sourcePostData['domain']] = 0

        # Собираем все релавантные текста и ссылки, 
        # для исходного поста 
        listOfRelevantPosts = []
        for relevantPost in scoreList:
            relevantPostData = listOfTexts[relevantPost[2]]

            listOfRelevantPosts.append([
                relevantPostData['title'], 
                hugo.getPostPermaLink(relevantPostData['domain'], 
                                      relevantPostData['filePath'])
            ])

        ressultWriting = textSites.writeLinksToPost(sourcePostData['filePath'],
                                   listOfRelevantPosts)

        # Подсчет добленных ссылок для таблици
        if ressultWriting:
            ressultData[sourcePostData['domain']] += len(listOfRelevantPosts)
    
    # Вывод таблици
    print('\n')
    print(tabulate(ressultData.items(), ['Domain', 'Added Relevant Links'], 
                   tablefmt="github"))
    print('\n')

if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    path_to_list = args.list if args.list else '/'

    if Path(path_to_list).exists():
        os.environ['TOKENIZERS_PARALLELISM'] = 'true'
        main()
    else:
        raise FileNotFoundError(
            f'{path_to_list} not found!'
        )