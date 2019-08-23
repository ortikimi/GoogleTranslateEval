from yap.yapParser import parse
from google_api.translator import GoogleTranslator
from cky.ckyParser import CKYParser


class Evaluator:
#     init_ted_talks()
#     sentence = "I want to sleep"
#     translated = GoogleTranslator.translate(sentence, 'en', 'he')
#     parse(translated.text)
#     evaluate_eng_to_heb('','I saw a telescope');
    parser = CKYParser()
    eng_tag = parser.parseSentence('Elad saw 8 telescopes')
    print(eng_tag)
    
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
