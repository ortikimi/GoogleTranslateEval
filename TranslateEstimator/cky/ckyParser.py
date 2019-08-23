from functools import reduce
import sys, time
import nltk
from nltk import induce_pcfg
from nltk import tokenize
from nltk import treetransforms
from nltk import pos_tag
from nltk.corpus import treebank
from nltk.grammar import PCFG, Nonterminal, toy_pcfg1
from nltk.parse import ViterbiParser
from nltk.parse import pchart


class CKYParser:

    def get_missing_words(self, grammar, words):
        """
        Find list of missing words not covered by grammar
        """
        missing = [word for word in words
                   if not grammar._lexical_index.get(word)]
        return missing
    
    def createGrammar(self, unkownWords):
        print("Induce PCFG grammar from treebank data:")
        productions = []
        for item in treebank.fileids():
          for tree in treebank.parsed_sents(item):
            # perform optional tree transformations, e.g.:
            tree.collapse_unary(collapsePOS=False)  # Remove branches A-B-C into A-B+C
            tree.chomsky_normal_form(horzMarkov=2)  # Remove A->(B,C,D) into A->B,C+D->D
            productions += tree.productions()
        for word in unkownWords:
            tag = pos_tag([word])[0][1]
            productions.append(nltk.grammar.Production(Nonterminal(tag), (word,)))
        S = Nonterminal('S')
        grammar = induce_pcfg(S, productions)
        return grammar

    def parseSentence(self, sent):
        
        grammar = self.createGrammar(set())
                
        # Tokenize the sentence.
        words = sent.split()
        
        unknown_words = self.get_missing_words(grammar, words);
        
        if(unknown_words != []):
            grammar = self.createGrammar(unknown_words)
        # Define a list of parsers.  We'll use all parsers.
        parsers = [
        ViterbiParser(grammar),
        ]
        
        times = []
        average_p = []
        num_parses = []
        all_parses = {}
        for parser in parsers:
            print('\ns: %s\nparser: %s\ngrammar: %s' % (sent, parser, grammar))
            parser.trace(3)
            t = time.time()
            parses = parser.parse_all(words)
            times.append(time.time() - t)
            if parses: 
                lp = len(parses)
                p = reduce(lambda a, b:a + b.prob(), parses, 0.0)
            else: 
                p = 0
            average_p.append(p)
            num_parses.append(len(parses))
            for p in parses: 
                all_parses[p.freeze()] = 1
        
        # Print summary statistics
        print()
        print('-------------------------+------------------------------------------')
        print('   Parser           Beam | Time (secs)   # Parses   Average P(parse)')
        print('-------------------------+------------------------------------------')
        for i in range(len(parsers)):
            print('%19s %4d |%11.4f%11d%19.14f' % (parsers[i].__class__.__name__,
              getattr(parsers[0], "beam_size", 0),
              times[i],
              num_parses[i],
              average_p[i]))
        parses = all_parses.keys()
        if parses: 
            p = reduce(lambda a, b:a + b.prob(), parses, 0) / len(parses)
        else: 
            p = 0
        print('-------------------------+------------------------------------------')
        print('%19s      |%11s%11d%19.14f' % ('(All Parses)', 'n/a', len(parses), p))
        print()
        
        for parse in parses:
            print(parse)
        
        return parse.pos()
