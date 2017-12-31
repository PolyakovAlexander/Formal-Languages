from collections import defaultdict
import sys
import re


# grammar in Chomsky normal form
class GrammarChomsky:
    def __init__(self):
        self.rules = defaultdict(list)


# graph-like grammar
class Grammar:
    def __init__(self):
        self.edges = None
        self.starts = defaultdict()
        self.finals = defaultdict()
        self.terminals = set()
        self.non_terminals = set()
        self.length = 0

def parse_chomsky_grammar(file):

    try:
        f = open(file, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    grammar = GrammarChomsky()

    for line in f:
        splitted = line.strip().split(' -> ')
        grammar.rules[splitted[0]] += [splitted[1]]

    f.close()

    return grammar


def parse_grammar(file):

    try:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    grammar = Grammar()
    size = lines[2].count(';')
    vertex = lines[2].split(';')[:-1]
    grammar.edges = []
    grammar.length = size

    for line in lines[3:]:
        line = line.replace(" -> ", '->')
        line = line.replace(" = ", '=')

        # fill start states
        line_ = re.findall('(\d+)\[label="(\w+)", \w*color="green"\]', line)
        if line_:
            state, nonterminal = line_[0]
            grammar.starts[int(state)] = nonterminal

        # fill final states
        line_ = re.findall('(\d+)\[label="(\w+)", shape="doublecircle"*', line)
        if line_:
            state, nonterminal = line_[0]
            grammar.finals[int(state)] = nonterminal

        # fill grammar
        line_ = re.findall('(\d+)->(\d+)\[label="(\w+|.)"\]', line)
        if line_:
            i, j, label = line_[0]
            grammar.edges.append((int(i), int(j), label))
            if not label.isupper():
                grammar.terminals.add(label)
            else:
                grammar.non_terminals.add(label)

    return grammar, vertex


def parse_graph(file, gll=False):

    try:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    size = lines[2].count(';')
    vertex = lines[2].split(';')[:-1]
    matrix = []
    for line in lines:
        splitted = line.split()
        if '->' in splitted:
            digits = re.findall(r'\d+', splitted[2])
            src_node = splitted[0]
            dst_node = digits[0]
            label = splitted[2].split('label="')[1].split('"')[0]
            matrix.append((src_node, dst_node, label))

    if gll:
        graph = defaultdict(set)
        for src, dst, label in matrix:
            graph[int(src)].add((int(dst), label))

        return graph

    return matrix, size, vertex
