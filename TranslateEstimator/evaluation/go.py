from sys import argv
from evaluation.processEvaluator import ProcessEvaluator

def gohe():
    print()
    print("==========")
    print("Evaluting translation of google translate from Hebrew to English")
    print()
    eval = ProcessEvaluator('he', 'en')
    eval.evaluate()

def goen():
    print()
    print("==========")
    print("Evaluting translation of google translate from English to Hebrew")
    print()
    eval = ProcessEvaluator('en', 'he')
    eval.evaluate()

def checkInput(source_lang, dest_lang, sentence):
    if source_lang != 'he' and source_lang != 'en':
        print('Unsupported source language. Supported languages are English and Hebrew')
        return False
    if dest_lang != 'he' and dest_lang != 'en':
        print('Unsupported destination language. Supported languages are English and Hebrew')
        return False
    if len(sentence) < 2:
        print('Wrong sentence format. Please try again')
        return False
    return True


def goSingleSentence(source_lang, dest_lang, sentence):
    if checkInput(source_lang, dest_lang, sentence) == False:
        return
    print()
    print("==========")
    print("Evaluting translation of a given sentence")
    print()
    eval = ProcessEvaluator(source_lang, dest_lang, sentence)
    eval.evaluate()

def goall():
    print()
    print("==========")
    print("Translating from Hebrew to English and vice versa")
    gohe()
    goen()

def print_usage():
    print()
    print("Usage:")
    print('python go.py he - translates hebrew sentences to english sentences using exiting corpus.')
    print('python go.py en - translates english sentences to hebrew sentences using exiting corpus.')
    print('python go.py all translates english sentences to hebrew and vice versa')
    print('python go.py <source_lang> <dest_lang> <sentence> - translates given sentence without gold evaluation')
    print()


print_usage()
if len(argv) == 2:
    if argv[1] == 'he':
        gohe()
    elif argv[1] == 'en':
        goen()
    elif argv[1] == 'all':
        goall()
elif len(argv) > 2:
    sentence = " ".join(argv[3::])
    goSingleSentence(argv[1], argv[2], sentence)
else:
    print_usage()
