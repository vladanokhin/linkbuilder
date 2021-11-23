import argparse
from text import Text
from pathlib import Path
from ss import SemanticSimilarity


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', type=str, required=True,
        help="Путь к списку с доменами, обезательный. (path/to/list.txt)"
    )     

    return parser

def main():
    textSites = Text()
    semanticSimilarity = SemanticSimilarity(textSites)

    with open(path_to_list) as f:
        lines = f.readlines()
    
    # Собираем текста со всех сайтов
    listTexts = list()
    for line in lines:
        site = line.strip()
        textFromSite = textSites.getTextFromSite(site)

        if textFromSite:
            listTexts.extend(textFromSite)
    
    # with open('.data.json', 'w', encoding='utf-8') as output:    
    #     output.write(json.dumps(listTexts, indent=4, sort_keys=True))

    # Сематическое сравнение текстов между собой
    semanticSimilarity.textComparison(listTexts)

    print(semanticSimilarity.getRelavantPages(3))


if __name__ == '__main__':

    parser = createParser()
    args = parser.parse_args()
    path_to_list = args.list if args.list else None

    if Path(path_to_list).exists():
        main()
    else:
        raise FileNotFoundError(
            f'{path_to_list} not found!'
        )