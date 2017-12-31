import parsers
import argparse
import copy


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


def matrix_algorithm(gram_path, graph_path, out=None, test=False):
    grammar = parsers.parse_chomsky_grammar(gram_path).rules
    graph, N = parsers.parse_graph(graph_path)
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
    else:
        if out is None:
            for (i, non_term, j) in res:
                print(str(i) + ',' + non_term + ',' + str(j))
        else:
            with open(args.out_path, 'w') as f:
                for (i, non_term, j) in res:
                    f.write(str(i) + ',' + non_term + ',' + str(j) + '\n')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--gram', dest='gram_path', type=str,
                        help='Path to file with grammar')
    parser.add_argument('--graph', dest='graph_path', type=str,
                        help='Path to file with graph/automaton')
    parser.add_argument('--out', dest='out_path', type=str,
                        help='Path to file to store the results(optional)')
    args = parser.parse_args()

    matrix_algorithm(args.gram_path, args.graph_path, args.out_path)
