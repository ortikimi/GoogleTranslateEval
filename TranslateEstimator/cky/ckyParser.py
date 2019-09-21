import spacy

class CKYParser:

    def parseSentence(self, sentence):
        nlp = spacy.load("en_core_web_sm") 
        parse = nlp(sentence)
        pos_tags = [['' + str(i) + '', i.tag_] for i in parse]

        return pos_tags
