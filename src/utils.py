from collections import defaultdict
import sys
import re


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
    grammar.edges = []

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

    return grammar


def parse_graph(file):

    try:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    size = lines[2].count(';')
    matrix = []
    for line in lines:
        splitted = line.split()
        if '->' in splitted:
            digits = re.findall(r'\d+', splitted[2])
            src_node = splitted[0]
            dst_node = digits[0]
            label = splitted[2].split('label="')[1].split('"')[0]
            matrix.append((src_node, dst_node, label))

    return matrix, size


def path_add(matrix, start, final, s, rules):
    for lp, rp in rules.items():
        if s == lp:
            matrix[start, final].update(rp)


def dfs(matrix, start_pos, cur_pos, s, rules, depth=1):
    path_add(matrix, start_pos, cur_pos, s, rules)
    if depth == 0:
        return

    n = len(matrix)
    for i in filter(lambda x: bool(matrix[cur_pos, x]), range(n)):
        letters = matrix[cur_pos, i].copy()
        for item in letters:
            dfs(matrix, start_pos, i, s + item, rules, depth - 1)