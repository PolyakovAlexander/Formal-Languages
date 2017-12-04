import re, sys


def parse_graph(path):

    try:
        f = open(path, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    lines = f.readlines()

    graph = []
    N = lines[2].count(';')
    for line in lines:
        splitted = line.split()
        if '->' in splitted:
            digits = re.findall(r'\d+', splitted[2])
            src_node = splitted[0]
            dst_node = digits[0]
            label = digits[1]
            graph.append((src_node, dst_node, label))

    return graph, N