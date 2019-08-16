from functools import reduce
import sys, time

from nltk import tokenize
from nltk.grammar import toy_pcfg1
from nltk.parse import ViterbiParser
from nltk.parse import pchart

demos = [('I saw John with my telescope', toy_pcfg1)]
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
