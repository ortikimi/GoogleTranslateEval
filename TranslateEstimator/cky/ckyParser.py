from functools import reduce
import sys, time

from nltk import induce_pcfg
from nltk import pos_tag
from nltk import tokenize
from nltk import treetransforms
import nltk
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
        parser = ViterbiParser(grammar)
        
        #print('\ns: %s\nparser: %s\ngrammar: %s' % (sent, parser, grammar))
        #parser.trace(3)
        parses = parser.parse_all(words)
        
        for parse in parses:
            print(parse)
        
        return parse.pos()
