import json
import argparse
from hugo import Hugo
from text import Text
from pathlib import Path
from semantic import SemanticSimilarity


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', type=str, required=False,
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
        textFromSite = textSites.getTextFromSite(site)
        if textFromSite:
            listOfTexts.extend(textFromSite)

    with open('.data.json', 'w', encoding='utf-8') as output:    
        output.write(json.dumps(listOfTexts, indent=4, sort_keys=True))

    # Сематическое сравнение текстов между собой
    semanticSimilarity.textComparison(listOfTexts)

    for id in range(0, len(listOfTexts)):
        scoreList = semanticSimilarity.getRelavantPages(id)
        if not scoreList:
            continue

        sourcePostData = listOfTexts[id]
        listOfRelevantPosts = []
        # Собираем все релавантные посты,
        for relevantPost in scoreList:
            relevantPostData = listOfTexts[relevantPost[2]]

            listOfRelevantPosts.append([
                relevantPostData['title'], 
                hugo.getPostPermaLink(relevantPostData['domain'], 
                                      relevantPostData['filePath'])
            ])
        
        print(listOfRelevantPosts)
        breakpoint()
        # textSites.addLinksToPost(sourcePostData['filepath'],
        #                          listOfRelevantPosts)



if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    path_to_list = args.list if args.list else 'list.txt'

    if Path(path_to_list).exists():
        main()
    else:
        raise FileNotFoundError(
            f'{path_to_list} not found!'
        )