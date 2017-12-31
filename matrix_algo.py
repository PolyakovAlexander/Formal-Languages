import utils
import copy
import sys


def matrix_closure(matrix, grammar, n):

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for T1 in matrix[i][j]:
                    for T2 in matrix[j][k]:
                        for left, right in grammar.items():
                            for value in right:
                                if T1 + ' ' + T2 == value and left not in matrix[i][k]:
                                    matrix[i][k].append(left)

    return matrix


def matrix_algorithm(graph_path, gram_path, out=None, test=False, custom_test=False):
    grammar = utils.parse_chomsky_grammar(gram_path).rules
    graph, N, _ = utils.parse_graph(graph_path)
    matrix = [[[] for i in range(N)] for j in range(N)]

    for (i, j, label) in graph:
        for left, right in grammar.items():
            for value in right:
                if value == label:
                    matrix[int(i)][int(j)].append(left)

    old_matrix = ['!@#$%']

    while old_matrix != matrix:
        old_matrix = copy.deepcopy(matrix)
        updated = matrix_closure(copy.deepcopy(matrix), grammar, N)
        for i in range(N):
            for j in range(N):
                matrix[i][j] += updated[i][j]
                matrix[i][j] = list(set(matrix[i][j]))

    res = []
    res_count = 0

    for i in range(N):
        for j in range(N):
            for non_term in matrix[i][j]:
                if test and non_term == 'S':
                    res_count += 1
                else:
                    res.append((i, non_term, j))

    if test:
        return res_count
    elif custom_test:
        return list(filter(lambda x: x[1] == 'S', res))
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
