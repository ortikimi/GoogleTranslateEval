from googletrans import Translator


class GoogleTranslator():

    def translate(sentence, srcLan, desnLang):
        translator = Translator()
        return translator.translate(sentence, dest=desnLang, src=srcLan)
