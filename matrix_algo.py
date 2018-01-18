import utils
import copy
import sys


def matrix_closure(matrix, grammar, n):

    changes = False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for T1 in matrix[i][j]:
                    for T2 in matrix[j][k]:
                        for left, right in grammar.items():
                            for value in right:
                                if T1 + ' ' + T2 == value and left not in matrix[i][k]:
                                    matrix[i][k].append(left)
                                    changes = True

    return changes, matrix


def matrix_algorithm(graph_path, gram_path, out=None, test=False):
    G = utils.parse_chomsky_grammar(gram_path)
    grammar = G.rules
    graph, n, _ = utils.parse_graph(graph_path)
    matrix = [[[] for i in range(n)] for j in range(n)]

    for (i, j, label) in graph:
        for left, right in grammar.items():
            for value in right:
                if value == label:
                    matrix[int(i)][int(j)].append(left)

    # Add loops if there is rules like A -> eps in grammar
    for i in range(n):
        matrix[i][i] += G.eps_nonterms

    old_matrix = ['!@#$%']

    is_changing = True
    while is_changing:
        is_changing, matrix = matrix_closure(matrix, grammar, n)

    res = set()
    res_count = 0

    for i in range(n):
        for j in range(n):
                if test and 'S' in matrix[i][j]:
                    res_count += 1
                else:
                    for non_term in matrix[i][j]:
                        res.add((i, non_term, j))

    if test:
        return res_count
    else:
        if out is None:
            for (i, non_term, j) in res:
                print(str(i) + ',' + non_term + ',' + str(j))
        else:
            with open(out, 'w') as f:
                for (i, non_term, j) in res:
                    f.write(str(i) + ',' + non_term + ',' + str(j) + '\n')

if __name__ == '__main__':

    if len(sys.argv) == 4:
        matrix_algorithm(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        matrix_algorithm(sys.argv[1], sys.argv[2])
    else:
        print('Incorrect amount of arguments, run script like this: '
              'python3 matrix_algo.py [automaton] [grammar] [output]')
