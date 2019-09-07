import csv

from nltk.translate.bleu_score import sentence_bleu

from Common.eval_result import EvalResult
from Wikipedia.wikipedia import get_parallel_corpus
from evaluation.translateEvaluator import TranslateEvaluator
from google_api.translator import GoogleTranslator
from tagging.tagger import Tagger


LIMIT_PARSER = 10


class Solution:
    
    def __init__(self, source_language, destination_language, sentence=None):
        self.source_language = source_language
        self.destination_language = destination_language
        self.sentence = sentence

    def evaluate(self):
        googleTranslator = GoogleTranslator(self.source_language, self.destination_language)
        evaluator = TranslateEvaluator(self.source_language, self.destination_language)
        tagger = Tagger()
        results = []

        # If we recieved only one sentence
        if (self.sentence != None):
            src_sentences = [self.sentence]
            dst_sentences = [' ']
            translated_sentences = [googleTranslator.translate(self.sentence).text]
            if (self.source_language == 'he'):
                tagged_src_sentences = tagger.tag_heb_sentences(src_sentences)
                tagged_dst_sentences = tagger.tag_eng_sentences(translated_sentences)
            else:
                tagged_src_sentences = tagger.tag_eng_sentences(src_sentences)
                tagged_dst_sentences = tagger.tag_heb_sentences(translated_sentences)
        # Else parse all the sentences
        else:
            multi_lingual_sentences = get_parallel_corpus()[:LIMIT_PARSER]
            heb_sentences = list(map(lambda sent : sent.heb_sentence, multi_lingual_sentences))
            eng_sentences = list(map(lambda sent:  sent.en_sentence, multi_lingual_sentences))
            if (self.source_language == 'he'):
                src_sentences = heb_sentences
                dst_sentences = eng_sentences
                tagged_src_sentences = tagger.tag_heb_sentences(heb_sentences)
                translated_sentences = list(map(lambda sent : googleTranslator.translate(sent).text, heb_sentences))
                tagged_dst_sentences = tagger.tag_eng_sentences(translated_sentences)
            else:
                src_sentences = eng_sentences
                dst_sentences = heb_sentences
                tagged_src_sentences = tagger.tag_eng_sentences(eng_sentences)
                translated_sentences = list(map(lambda sent : googleTranslator.translate(sent).text, eng_sentences))    
                tagged_dst_sentences = tagger.tag_heb_sentences(translated_sentences)
            
        for idx,tagged_sent in enumerate(tagged_src_sentences):
            result = EvalResult(src_sentences[idx], translated_sentences[idx])
            result.set_eval_score(evaluator.evaluate_pos_tagging(tagged_sent, tagged_dst_sentences[idx]))
            result.set_gold_sentence(dst_sentences[idx])
            if (self.source_language == 'he'):
                result.set_english_tag(tagged_dst_sentences[idx])
                result.set_hebrew_tag(tagged_sent)
            else:
                result.set_english_tag(tagged_sent)
                result.set_hebrew_tag(tagged_dst_sentences[idx])
            self.set_bleu_score(dst_sentences[idx], translated_sentences[idx], result)
            results.append(result)

        self.write_spreadsheet(results)
    
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

