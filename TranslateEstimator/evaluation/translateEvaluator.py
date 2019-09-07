

class TranslateEvaluator:

    def __init__(self, source_language, destination_language):
        self.source_language = source_language
        self.destination_language = destination_language
     
    def evaluate_pos_tagging(self, src_tags, dst_tags):
        eval_of_dst = 0
        eval_of_src = 0;
        listOfTags = [
            {
                'Tag':'VERB',
                'Weight': 1,
                'en': ('VB','VBD','VBG','VBN'),
                'he' : ('BN')
                },
            {
                'Tag':'PRONOUN',
                'Weight': 0.5,
                'en': ('PRP'),
                'he' : ('PRP')
                },
            {
                'Tag':'NAME',
                'Weight': 1,
                'en': ('NNP','NNPS'),
                'he' : ('NNP')
                },
            {
                'Tag':'COP',
                'Weight': 0.5,
                'en': ('VBZ,VBP'),
                'he' : ('COP')
                },
            {
                'Tag':'DET',
                'Weight': 0.1,
                'en': ('DT'),
                'he' : ('REL','DEF')
                },
            {
                'Tag':'NUMBER',
                'Weight': 1,
                'en': ('CD'),
                'he' : ('NCD')
                },
            {
                'Tag':'NOUN',
                'Weight': 0.2,
                'en': ('NN','NNS'),
                'he' : ('NN, NNT')
                },
            {
                'Tag':'ADJECTIVE',
                'Weight': 0.2,
                'en': ('JJ'),
                'he' : ('JJ')
                },
            {
                'Tag':'ADP',
                'Weight': 0.1,
                'en': ('IN'),
                'he' : ('IN','POS')
                },
            {
                'Tag':'AND',
                'Weight': 0.1,
                'en': ('CC'),
                'he' : ('CONJ')
                }
        ]
        
        for tag in listOfTags:
            numOfSrcTags = sum(item[1] in tag[self.source_language] for item in src_tags)
            eval_of_src += tag['Weight'] * numOfSrcTags
            numOfDstTags = sum(item[1] in tag[self.destination_language] for item in dst_tags)
            eval_of_dst += tag['Weight'] * numOfDstTags
        
        if(eval_of_src == 0 or eval_of_dst == 0):
            return 0
        else: 
            print('***eval_of_dst*****')
            if (eval_of_src < eval_of_dst):
                return eval_of_src / eval_of_dst
            else:
                return eval_of_dst / eval_of_src

