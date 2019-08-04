from googletrans import Translator


class GoogleTranslator():

    def translate(self, sentence):
        translator = Translator()
        translator.translate(sentence, dest='en', src='he')
