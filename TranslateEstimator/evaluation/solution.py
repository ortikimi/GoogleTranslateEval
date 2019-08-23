from TranslateEstimator.yap.yapParser import parse
from TranslateEstimator.google_api.translator import GoogleTranslator
from TranslateEstimator.Wikipedia.wikipedia import get_parallel_corpus

LIMIT_PARSER = 10

class Solution:

    #multi_lingual_sentences = get_parallel_corpus()
    count = 0
    translated = GoogleTranslator.translate("I want to sleep", 'en', 'he')
    parse(translated.text)

    # for sentence in multi_lingual_sentences:
    #     if (count == LIMIT_PARSER):
    #         print('finish')
    #         break
    #     count += 1
    #     translated = GoogleTranslator.translate(sentence.en_sentence, 'en', 'he')
    #     print('Translating English Text')
    #     print(sentence.en_sentence)
    #     print('Parsing hebrew text')
    #     parse(translated.text)
