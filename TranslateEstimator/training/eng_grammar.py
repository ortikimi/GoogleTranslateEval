import nltk
from nltk.corpus import treebank
from nltk.grammar import CFG, Nonterminal


def createGrammar():
    tbank_productions = set(production for sent in treebank.parsed_sents()
                            for production in sent.productions())
    return CFG(Nonterminal('S'), list(tbank_productions))
