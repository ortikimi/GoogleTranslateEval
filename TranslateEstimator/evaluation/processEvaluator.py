from Wikipedia.wikipedia import get_parallel_corpus
from cky.ckyParser import CKYParser
from google_api.translator import GoogleTranslator
from yap.yapParser import parse
from Common.eval_result import EvalResult
from nltk.translate.bleu_score import sentence_bleu
import csv

LIMIT_PARSER = 1


class ProcessEvaluator:
    
    def __init__(self, source_language, destination_language, sentence=None):
        self.source_language = source_language
        self.destination_language = destination_language
        self.sentence = sentence

    def evaluate(self):
        googleTranslator = GoogleTranslator()
        results = []

        if (self.sentence != None):
            translated = googleTranslator.translate(self.sentence, self.source_language, self.destination_language)
            self.tagging_sentence(self.sentence, translated.text)
            return

        multi_lingual_sentences = get_parallel_corpus()
        count = 0

        for sentence in multi_lingual_sentences:
            if (count == LIMIT_PARSER):
                print('finish')
                break
            count += 1
            if (self.source_language == 'he'):
                original_sentence = sentence.heb_sentence
                gold_text = sentence.en_sentence
            else:
                original_sentence = sentence.en_sentence
                gold_text = sentence.heb_sentence
            print('Translating %s Text' % self.source_language)
            print(original_sentence)
            translated = googleTranslator.translate(original_sentence, self.source_language, self.destination_language)
            result = self.tagging_sentence(original_sentence, translated.text)
            result.set_gold_sentence(gold_text)
            self.set_bleu_score(gold_text, translated.text, result)
            results.append(result)

        self.write_spreadsheet(results)

    def tagging_sentence(self, original_text, translated_text):
        result = EvalResult(original_text, translated_text)
        eng_parser = CKYParser()
        print('Tagging the givern sentence')
        if (self.source_language == 'he'):
            heb_tag = parse(original_text)
            print('Tagging the translated sentence')
            eng_tag = eng_parser.parseSentence(translated_text)
            score = self.evaluate_pos_tagging(heb_tag, eng_tag)
        else:
            eng_tag = eng_parser.parseSentence(original_text)
            print('Tagging the translated sentence')
            heb_tag = parse(translated_text)
            score = self.evaluate_pos_tagging(eng_tag, heb_tag)
        
        result.set_english_tag(eng_tag)
        result.set_hebrew_tag(heb_tag)
        result.set_eval_score(score)
        return result

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
        
        return (score / num_of_parameters) * 100

    def set_bleu_score(self, gold_sentence, translated_text, result):
        gold_words = [gold_sentence.split()]
        translated_words = translated_text.split()
        score_1ngram = sentence_bleu(gold_words, translated_words, weights=(1, 0, 0, 0))
        score_2ngram = sentence_bleu(gold_words, translated_words, weights=(0.5, 0.5, 0, 0))
        result.set_bleu_1ngram_score(format(score_1ngram, '.8f'))
        result.set_bleu_2ngram_score(format(score_2ngram, '.8f'))

    def write_spreadsheet(self, results):
        file_name = 'translated' + self.source_language + '.csv'
        with open(file_name, encoding='utf-16', mode='w') as lang_file:
            results_writer = csv.writer(lang_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            results_writer.writerow(['Original Sentence', 'Translated Sentence', 'Gold translated Sentence',
                                      'Hebrew Tagging', 'English Tagging', 'Evaluation Result', 'Bleu Result 1 ngram', 'Bleu Result 2 ngram'])
            for r in results:
                results_writer.writerow([r.original_sentence, r.translated_sentence, r.gold_sentence,
                                        r.hebrew_tag, r.english_tag, r.score, r.bleu_1ngram_score, r.bleu_2ngram_score])

