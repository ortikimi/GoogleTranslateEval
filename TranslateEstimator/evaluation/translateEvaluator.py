

class TranslateEvaluator:

    def __init__(self, source_language, destination_language):
        self.source_language = source_language
        self.destination_language = destination_language
     
    def evaluate_pos_tagging(self, src_tags, dst_tags):
        eval_of_dst = 0
        eval_of_src = 0
        src_tags_output = "Source: \n"
        dst_tags_output = "Destination: \n"
        listOfTags = [
            {
                'Tag':'VERB',
                'Weight': 1,
                'en': ('VB', 'VBG', 'VBN', 'MD'),
                'he' : ('VB', 'BN', 'MD')
                },
            {
                'Tag':'PRONOUN',
                'Weight': 0.5,
                'en': ('PRP', ' PRP$'),
                'he' : ('PRP', ' S_PRN')
                },
            {
                'Tag':'NAME',
                'Weight': 1,
                'en': ('NNP', 'NNPS'),
                'he' : ('NNP',)
                },
            {
                'Tag':'COP',
                'Weight': 0.5,
                'en': ('VBD', 'VBZ', 'VBP'),
                'he' : ('COP',)
                },
            {
                'Tag':'DET',
                'Weight': 0.1,
                'en': ('DT',),
                'he' : ('REL', 'DEF')
                },
            {
                'Tag':'NUMBER',
                'Weight': 1,
                'en': ('CD'),
                'he' : ('CD', 'NCD')
                },
            {
                'Tag':'NOUN',
                'Weight': 0.2,
                'en': ('NN', 'NNS'),
                'he' : ('NN', ' NNT')
                },
            {
                'Tag':'ADJECTIVE',
                'Weight': 0.2,
                'en': ('JJ', 'JJS'),
                'he' : ('JJ',)
                },
            {
                'Tag':'RB',
                'Weight': 0.2,
                'en': ('RB',),
                'he' : ('RB',)
                },
            {
                'Tag':'ADP',
                'Weight': 0.1,
                'en': ('IN',),
                'he' : ('IN', 'POS', 'PREPOSITION')
                },
            {
                'Tag':'AND',
                'Weight': 0.1,
                'en': ('CC',),
                'he' : ('CONJ',)
                },
            {
                'Tag':'EXIST',
                'Weight': 0.1,
                'en': ('EX',),
                'he' : ('EX',)
                }
        ]
        
        for tag in listOfTags:
            numOfSrcTags = sum(item[1] in tag[self.source_language] for item in src_tags)
            src_tags_output = src_tags_output + "#" + tag['Tag'] + " : " + str(numOfSrcTags) + "\n";
            eval_of_src += tag['Weight'] * numOfSrcTags
            numOfDstTags = sum(item[1] in tag[self.destination_language] for item in dst_tags)
            dst_tags_output = dst_tags_output + "#" + tag['Tag'] + " : " + str(numOfDstTags) + "\n";
            eval_of_dst += tag['Weight'] * numOfDstTags
        
        if(eval_of_src == 0 or eval_of_dst == 0):
            return 0
        else: 
            if (eval_of_src < eval_of_dst):
                return {'score': eval_of_src / eval_of_dst, 'num_of_tags':  src_tags_output + dst_tags_output}
            else:
                return {'score': eval_of_dst / eval_of_src, 'num_of_tags':  src_tags_output + dst_tags_output}

