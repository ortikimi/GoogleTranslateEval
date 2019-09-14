import os
from translate.storage.tmx import tmxfile
from Common.multi_lingual_sentence import MultiLingualSentence

'''For future work, working with OPUS corpus'''

WIKIPEDIA_FILE = 'corpus.tmx'

def get_parallel_corpus():
    multi_lingual_sentences = []
    location = os.path.join(os.path.dirname(os.path.realpath(__file__)),WIKIPEDIA_FILE)
    with open(location, 'rb') as fin:
        tmx_file = tmxfile(fin, 'en', 'he')
        for node in tmx_file.unit_iter():
            sentence = MultiLingualSentence(node.gettarget(), node.getsource())
            multi_lingual_sentences.append(sentence)

    return multi_lingual_sentences