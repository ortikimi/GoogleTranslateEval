from googletrans import Translator


class GoogleTranslator():

    def translate(self, sentence, srcLan, desnLang):
        translator = Translator()
        return translator.translate(sentence, dest=desnLang, src=srcLan)
