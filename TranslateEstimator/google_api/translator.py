from googletrans import Translator


class GoogleTranslator():

    def __init__(self, source_language, destination_language):
        self.source_language = source_language
        self.destination_language = destination_language

    def translate(self, sentence):
        translator = Translator()
        return translator.translate(sentence, dest=self.destination_language, src=self.source_language)
