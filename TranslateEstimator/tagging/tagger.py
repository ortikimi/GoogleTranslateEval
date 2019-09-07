from cky.ckyParser import CKYParser
from yap.yapParser import parse


class Tagger:
    
    def tag_eng_sentences(self, eng_sentences):
        eng_parser = CKYParser()
        parsed_sentences = []
        for sent in eng_sentences:
            parsed_sentences.append(eng_parser.parseSentence(sent))
        return parsed_sentences
            
    def tag_heb_sentences(self, heb_sentences):
        parsed_sentences = []
        for sent in heb_sentences:
            parsed_sentences.append(parse(sent))
        return parsed_sentences
