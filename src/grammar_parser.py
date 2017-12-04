import sys


def parse_grammar(path):

    try:
        f = open(path, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    grammar = []

    for line in f:
        splitted = line.strip().split(' -> ')
        grammar.append((splitted[0], splitted[1].replace(' ', '')))

    return grammar