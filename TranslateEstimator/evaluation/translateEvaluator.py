

class TranslateEvaluator:

    def __init__(self, source_language, destination_language):
        self.source_language = source_language
        self.destination_language = destination_language
     
    def evaluate_pos_tagging(self, src_tags, dst_tags):
        eval_of_dst = 0
        eval_of_src = 0
        src_tags_output = "Source: \n"
        dst_tags_output = "Destination: \n"
        listOfHeTags = {
            'VB':1,
            'MD':1,
            'BN':1,
            'PRP':0.5,
            'S_PRN':0.5,
            'NNP':1,
            'COP':0.5,
            'REL':0.1,
            'DEF':0.1,
            'CD':1,
            'NCD':1,
            'NN':0.2,
            'NNT':0.2,
            'JJ':0.2,
            'RB':0.2,
            'IN':0.1,
            'POS':0.1,
            'PREPOSITION':0.1,
            'CONJ':0.1,
            'EX':0.1
        }
    
        HeToEnTag = {
        'VB':['VB', 'VBG', 'VBN', 'MD'],
        'MD':['VB', 'VBG', 'VBN', 'MD'],
        'BN':['VB', 'VBG', 'VBN', 'MD'],
        'PRP':['PRP', ' PRP$'],
        'S_PRN':['PRP', ' PRP$'],
        'NNP':['NNP', 'NNPS'],
        'COP':['VBD', 'VBZ', 'VBP'],
        'REL':['DT', ],
        'DEF':['DT', ],
        'CD':['CD', ],
        'NCD':['CD', ],
        'NN':['NN', 'NNS'],
        'NNT':['NN', 'NNS'],
        'JJ':['JJ', 'JJS'],
        'RB':['RB', ],
        'IN':['IN', ],
        'POS':['IN', ],
        'PREPOSITION':['IN', ],
        'CONJ':['CC', ],
        'EX':['EX', ]
    }
        
        # Iterate over the tags of the source sentence - skip repeated tags.
        listOfUniqueSrcTags = set(map(lambda tag: tag[1], src_tags))
        
        for tag in listOfUniqueSrcTags:
            if(tag in listOfHeTags.keys()):
                numOfSrcTags = sum(item[1] == tag for item in src_tags)
                src_tags_output = src_tags_output + "#" + tag + " : " + str(numOfSrcTags) + "\n";
                eval_of_src += listOfHeTags[tag] * numOfSrcTags
                numOfDstTags = sum(item[1] in HeToEnTag[tag] for item in dst_tags)
                dst_tags_output = dst_tags_output + "#" + tag + " : " + str(numOfDstTags) + "\n";
                eval_of_dst += listOfHeTags[tag] * numOfDstTags
        
        if(eval_of_src == 0 or eval_of_dst == 0):
            return {'score': 0, 'num_of_tags':  src_tags_output + dst_tags_output}
        else: 
            if (eval_of_src < eval_of_dst):
                return {'score': eval_of_src / eval_of_dst, 'num_of_tags':  src_tags_output + dst_tags_output}
            else:
                return {'score': eval_of_dst / eval_of_src, 'num_of_tags':  src_tags_output + dst_tags_output}
