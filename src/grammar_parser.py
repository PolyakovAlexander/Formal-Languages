import sys
from collections import defaultdict


def parse_grammar(path):

    try:
        f = open(path, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    grammar = defaultdict(list)

    for line in f:
        splitted = line.strip().split(' -> ')
        grammar[splitted[0]] += [splitted[1]]

    return grammar
