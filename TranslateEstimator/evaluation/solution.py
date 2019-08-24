from Wikipedia.wikipedia import get_parallel_corpus
from cky.ckyParser import CKYParser
from google_api.translator import GoogleTranslator
from yap.yapParser import parse


LIMIT_PARSER = 1


class Evaluator:

    multi_lingual_sentences = get_parallel_corpus()
    googleTranslator = GoogleTranslator()
    parser = CKYParser()

    count = 0

    for sentence in multi_lingual_sentences:
        if (count == LIMIT_PARSER):
            print('finish')
            break
        count += 1
        translated = googleTranslator.translate(sentence.en_sentence, 'en', 'he')
        print('Translating English Text')
        print(sentence.en_sentence)
        print('Tagging the givern sentence')
        eng_tag = parser.parseSentence(sentence.en_sentence)
        print(eng_tag)
#         print('Parsing hebrew text')
#         print(translated.text)
# 

    
    def evaluate_eng_to_heb(self, heb_sent, eng_sent):
        parser = CKYParser()
        eng_tag = parser.parseSentence(eng_sent)
        heb_tag = []  # cky_of_an_hebrew_sentence(eng_sent)
        self.evaluate_pos_tagging(eng_tag, heb_tag)
     
    def evaluate_pos_tagging(self, src_tag, dst_tag):
        score = 0
        num_of_parameters = 0;
        
        numOfSrcVerbs = sum(p[0] in ('VB', 'VBD', 'VBG', 'VGN', 'VBP', 'VBZ') for p in src_tag)
        num_of_parameters += numOfSrcVerbs;
        numOfDstVerbs = sum(p[0] == 'VB' for p in dst_tag)
        score += numOfDstVerbs
        
        numOfSrcPronouns = sum(p[0] in ('PRP') for p in src_tag)
        num_of_parameters += numOfSrcPronouns;
        numOfDstPronouns = sum(p[0] == 'PRP' for p in dst_tag)
        score += numOfDstPronouns
        
        numOfSrcNums = sum(p[0] in ('CD') for p in src_tag)
        num_of_parameters += numOfSrcNums;
        numOfDstNums = sum(p[0] == 'CD' for p in dst_tag)
        score += numOfDstNums
