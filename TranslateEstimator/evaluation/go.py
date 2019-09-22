from sys import argv
from evaluation.solution import Solution

def gohe(optimize=False):
    print()
    print("==========")
    print("Evaluting translation of google translate from Hebrew to English")
    print()
    eval = Solution('he', 'en', optimize)
    eval.evaluate()

def goen(optimize=False):
    print()
    print("==========")
    print("Evaluting translation of google translate from English to Hebrew")
    print()
    eval = Solution('en', 'he', optimize)
    eval.evaluate()

def goall():
    print()
    print("==========")
    print("Translating from Hebrew to English and vice versa")
    gohe()
    goen()

def gooptimize():
    print()
    print("==========")
    print("Translating from Hebrew to English with optimized tagging.")
    gohe(True)

def print_usage():
    print()
    print("Usage:")
    print('python go.py he - translates Hebrew sentences to English sentences using exiting corpus.')
    print('python go.py en - translates English sentences to Hebrew sentences using exiting corpus.')
    print('python go.py all translates English sentences to Hebrew and vice versa')
    print('python go.py optimize translates Hebrew sentences to English sentences using exiting corpus and optimized parsing ')
    print()


print_usage()
if len(argv) == 2:
    if argv[1] == 'he':
        gohe()
    elif argv[1] == 'en':
        goen()
    elif argv[1] == 'all':
        goall()
    elif argv[1] == 'optimize':
        gooptimize()
else:
    print_usage()
