from sentence_transformers import SentenceTransformer, util
import json, argparse



model = SentenceTransformer('all-MiniLM-L6-v2')


with open('subnet1-texts.json') as f:
    sentences = json.loads(f.read())

paraphrases = util.paraphrase_mining(model, [i['content'] for i in sentences])

with open('subnet1-texts.txt', 'a', encoding='utf-8') as output:
    for paraphrase in paraphrases:
        score, i, j = paraphrase
        if sentences[i]['domain'] != sentences[j]['domain']:
            string = f'"{sentences[i]["filePath"]}";"{score}";"{sentences[j]["filePath"]}"\n'
            output.write(string)
