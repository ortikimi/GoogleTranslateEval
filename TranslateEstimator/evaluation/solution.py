from TranslateEstimator.yap.yapParser import parse
from TranslateEstimator.google_api.translator import GoogleTranslator
from TranslateEstimator.TED.tedTalks import init_ted_talks
class Solution:
    init_ted_talks()
    sentence = "I want to sleep"
    translated = GoogleTranslator.translate(sentence, 'en', 'he')
    parse(translated.text)
