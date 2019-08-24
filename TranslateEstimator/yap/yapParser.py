import requests
import json

DATA_FILE = "data.conllu"

def parse(sentence):

    ''' Get Yap parser results for the given sentence in hebrew'''
    newsentence = sentence + "  "
    headers = {'content-type': 'application/json'}
    data = {'text': newsentence}
    data_json = json.dumps(data)
    response = requests.get("http://localhost:8000/yap/heb/joint", data=data_json, headers=headers)
    json_data = json.loads(response.text)
    #(json_data['ma_lattice'])
    print(json_data['md_lattice'])

    ''' Parse results and insert relevant tagging into dictionary'''
    with open(DATA_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(json_data['md_lattice'])
    with open(DATA_FILE, encoding='utf-8') as fp:
        lines = fp.read().splitlines()
    tagging_dict = dict()
    for line in lines:
        if len(line) > 1:
            fields = line.split()
            if fields[2] not in tagging_dict:
                tagging_dict[fields[2]] = fields[4]
    print(tagging_dict)
    return tagging_dict
