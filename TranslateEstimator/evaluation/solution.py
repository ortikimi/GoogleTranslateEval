from TranslateEstimator.yap.yapParser import parse
from TranslateEstimator.google_api.translator import GoogleTranslator
from TranslateEstimator.Wikipedia.wikipedia import get_parallel_corpus
class Solution:
    multi_lingual_sentences = get_parallel_corpus()
    sentence = "I want to sleep"
    translated = GoogleTranslator.translate(sentence, 'en', 'he')
    parse(translated.text)
