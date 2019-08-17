from functools import reduce
import sys, time

from nltk import tokenize
import nltk
from nltk.corpus import treebank
from nltk.grammar import CFG, Nonterminal
from nltk.parse import ViterbiParser
from nltk.parse import pchart
from TranslateEstimator.training.eng_grammer import createGrammar


tbank_grammar = createGrammar()

demos = [('I saw John with my telescope', tbank_grammar)]
sent, grammar = demos[0]

# Tokenize the sentence.
tokens = sent.split()

# Run the parsers on the tokenized sentence.
times = []
average_p = []
num_parses = []
all_parses = {}
parser = ViterbiParser(grammar)
print('\ns: %s\nparser: %s\ngrammar: %s' % (sent, parser, grammar))
parser.trace(3)
t = time.time()
parses = parser.parse_all(tokens)
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

for parse in parses:
    print(parse)
