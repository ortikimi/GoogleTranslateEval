import ast
import codecs
import csv
import json

from nltk.translate.bleu_score import sentence_bleu

from Common.eval_result import EvalResult
from TED.tedTalksCSV import get_parallel_corpus
from evaluation.spredsheet_results import SpredSheetResults
from evaluation.translateEvaluator import TranslateEvaluator
from google_api.translator import GoogleTranslator
from tagging.tagger import Tagger


LIMIT_PARSER = 101
OPTIMIZED_HE_FILE = 'optimizedhe.csv'


class Solution:
    
    def __init__(self, source_language, destination_language, optimize=False, sentence=None):
        self.source_language = source_language
        self.destination_language = destination_language
        self.sentence = sentence
        self.optimize = optimize
        self.src_sentences = []
        self.gold_sentences = []
        self.translated_sentences = []
        self.tagged_src_sentences = []
        self.tagged_gold_sentences = []
        self.tagged_translated_sentences = []

    def evaluate(self):
        googleTranslator = GoogleTranslator(self.source_language, self.destination_language)
        tagger = Tagger()

        # If we recieved only one sentence
        if (self.sentence != None):
            src_sentences = [self.sentence]
            translated_sentences = [googleTranslator.translate(self.sentence).text]
            self.gold_sentences = [' ']
            if (self.source_language == 'he'):
                self.tagged_src_sentences = tagger.tag_heb_sentences(src_sentences)
                self.tagged_translated_sentences = tagger.tag_eng_sentences(translated_sentences)
            else:
                self.tagged_src_sentences = tagger.tag_eng_sentences(src_sentences)
                self.tagged_translated_sentences = tagger.tag_heb_sentences(translated_sentences)
        elif (self.optimize):
            if (self.source_language == 'he'):
                self.optimized_parser(OPTIMIZED_HE_FILE)
        # Else parse all the sentences
        else:
            multi_lingual_sentences = get_parallel_corpus()[:LIMIT_PARSER]
            heb_sentences = list(map(lambda sent : sent.heb_sentence, multi_lingual_sentences))
            eng_sentences = list(map(lambda sent:  sent.en_sentence, multi_lingual_sentences))
            if (self.source_language == 'he'):
                self.src_sentences = heb_sentences
                self.gold_sentences = eng_sentences
                self.tagged_src_sentences = tagger.tag_heb_sentences(self.src_sentences)
                self.translated_sentences = list(map(lambda sent : googleTranslator.translate(sent).text, self.src_sentences))
                self.tagged_translated_sentences = tagger.tag_eng_sentences(self.translated_sentences)
                self.tagged_gold_sentences = tagger.tag_eng_sentences(self.gold_sentences)
            else:
                self.src_sentences = eng_sentences
                self.gold_sentences = heb_sentences
                self.tagged_src_sentences = tagger.tag_eng_sentences(self.src_sentences)
                self.translated_sentences = list(map(lambda sent : googleTranslator.translate(sent).text, self.src_sentences))
                self.tagged_translated_sentences = tagger.tag_heb_sentences(self.translated_sentences)
                self.tagged_gold_sentences = tagger.tag_heb_sentences(self.gold_sentences)

        ''' Ebvalute translation and write results'''
        self.write_results()

    def optimized_parser(self, file_name):
        f = codecs.open(file_name, "rb", "utf-16")
        csvread = csv.reader(f, delimiter='\t')
        line_count = 0
        for row in csvread:
            if  line_count > 0 and len(row) > 0:
                self.src_sentences.append(row[0])
                self.translated_sentences.append(row[1])
                self.gold_sentences.append(row[2])
                self.tagged_src_sentences.append(ast.literal_eval(row[3]))
                self.tagged_translated_sentences.append(ast.literal_eval(row[4]))
                self.tagged_gold_sentences.append(ast.literal_eval(row[5]))
            line_count += 1

    def write_results(self):
        spredsheets_result = SpredSheetResults()
        evaluator = TranslateEvaluator(self.source_language, self.destination_language)
        results = []
        for idx, tagged_sent in enumerate(self.tagged_src_sentences):
            result = EvalResult(self.src_sentences[idx], self.translated_sentences[idx])
            google_tagged_obj = evaluator.evaluate_pos_tagging(tagged_sent, self.tagged_translated_sentences[idx])
            result.set_eval_score(google_tagged_obj['score'])
            result.set_google_comparison(google_tagged_obj['num_of_tags'])
            result.set_gold_sentence(self.gold_sentences[idx])
            gold_tagged_obj = evaluator.evaluate_pos_tagging(tagged_sent, self.tagged_gold_sentences[idx])
            result.set_gold_score(gold_tagged_obj['score'])
            result.set_gold_comparison(gold_tagged_obj['num_of_tags'])
            result.set_gold_tag(self.tagged_gold_sentences[idx])
            self.set_bleu_score(self.gold_sentences[idx], self.translated_sentences[idx], result)
            if (self.source_language == 'he'):
                result.set_english_tag(self.tagged_translated_sentences[idx])
                result.set_hebrew_tag(tagged_sent)
            else:
                result.set_english_tag(tagged_sent)
                result.set_hebrew_tag(self.tagged_translated_sentences[idx])
            results.append(result)

        spredsheets_result.write_spreadsheet(results, self.source_language)
        spredsheets_result.draw_graph()

    def set_bleu_score(self, gold_sentence, translated_text, result):
        gold_words = [gold_sentence.split()]
        translated_words = translated_text.split()
        score_1ngram = sentence_bleu(gold_words, translated_words, weights=(1, 0, 0, 0))
        score_2ngram = sentence_bleu(gold_words, translated_words, weights=(0.5, 0.5, 0, 0))
        result.set_bleu_1ngram_score(format(score_1ngram, '.8f'))
        result.set_bleu_2ngram_score(format(score_2ngram, '.8f'))

