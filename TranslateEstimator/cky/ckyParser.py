from functools import reduce
import sys, time

from nltk import induce_pcfg
from nltk import tokenize
from nltk import treetransforms
import nltk
from nltk.corpus import treebank
from nltk.grammar import PCFG, Nonterminal
from nltk.parse import ViterbiParser
from nltk.parse import pchart


def get_missing_words(grammar, words):
    """
    Find list of missing words not covered by grammar
    """
    missing = [word for word in words
               if not grammar._lexical_index.get(word)]
    return missing


def createGrammar(unkownWords):
    
    productions = []
    for item in treebank.fileids()[:2]:
        for tree in treebank.parsed_sents(item):
            # perform optional tree transformations, e.g.:
            tree.collapse_unary(collapsePOS=False)  # Remove branches A-B-C into A-B+C
            tree.chomsky_normal_form(horzMarkov=2)  # Remove A->(B,C,D) into A->B,C+D->D
            productions += tree.productions()
    for word in unkownWords:
        print(word)
        productions.append(nltk.grammar.Production(Nonterminal('NN'), (word,)))
    return induce_pcfg(Nonterminal('S'), list(productions))


# def parseSentence(sentence):
sent = 'I saw John with my telescope'
grammar = createGrammar(set())

# Tokenize the sentence.
tokens = sent.split()

# Run the parsers on the tokenized sentence.
times = []
average_p = []
num_parses = []
all_parses = {}
uknown_words = get_missing_words(grammar, 'I saw John with my telescope'.split())

if(uknown_words != []):
    grammar = createGrammar(uknown_words)

parser = ViterbiParser(grammar)
print('\ns: %s\nparser: %s\ngrammar: %s' % (sent, parser, grammar))
parser.trace(3)
parses = parser.parse_all(tokens)

for parse in parses:
    print(parse)
