import requests
import json

def parse(sentence):
    newsentence = sentence + "  "
    headers = {'content-type': 'application/json'}
    data = {'text': newsentence}
    data_json = json.dumps(data)

    response = requests.get("http://localhost:8000/yap/heb/joint", data=data_json, headers=headers)
    json_data = json.loads(response.text)
    print('ma_lattice')
    print(json_data['ma_lattice'])
    print('md_lattice')
    print(json_data['md_lattice'])
    print('dep_tree')
    print(json_data['dep_tree'])
