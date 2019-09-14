import os
import xlrd
from Common.multi_lingual_sentence import MultiLingualSentence

TED_FILE = 'ted_talks.xlsx'

def get_parallel_corpus():
    multi_lingual_sentences = []
    if os.path.isfile(TED_FILE) == False:
        print('Error opening TED talks file')
        return multi_lingual_sentences
    wb = xlrd.open_workbook(TED_FILE)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1,sheet.nrows):
        sentence = MultiLingualSentence(sheet.cell_value(i, 0), sheet.cell_value(i, 1))
        multi_lingual_sentences.append(sentence)
    return multi_lingual_sentences