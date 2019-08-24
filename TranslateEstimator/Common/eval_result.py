class EvalResult:

    def __init__(self, original_sentence, translated_sentence):
        self.original_sentence = original_sentence
        self.translated_sentence = translated_sentence
        self.score = 0
        self.blau_score = 0
        self.gold_sentence = ''
        self.hebrew_tag = ''
        self.english_tag = ''

    def set_eval_score(self, score):
        self.score = score

    def set_gold_sentence(self, sentence):
        self.gold_sentence = sentence

    def set_blau_score(self, blau_score):
        self.blau_score = blau_score

    def set_hebrew_tag(self, heb_tag):
        self.hebrew_tag = heb_tag

    def set_english_tag(self, en_tag):
        self.english_tag = en_tag

