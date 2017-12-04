import grammar_parser as gram
import graph_parser as gp
import matrix_closure as mc
import argparse
import copy


def matrix_algorithm(gram_path, graph_path, out=None, test=False):
    grammar = gram.parse_grammar(gram_path)
    graph, N = gp.parse_graph(graph_path)
    matrix = [[[] for i in range(0, N)] for j in range(0, N)]

    for (i, j, label) in graph:
        for (left, right) in grammar:
            if right == label:
                matrix[int(i)][int(j)].append(left)

    old_matrix = ['!@#$%']

    while old_matrix != matrix:
        old_matrix = copy.deepcopy(matrix)
        updated = mc.matrix_closure(copy.deepcopy(matrix), grammar, N)
        for i in range(0, N):
            for j in range(0, N):
                matrix[i][j] += updated[i][j]
                matrix[i][j] = list(set(matrix[i][j]))

    res = []
    res_count = 0

    for i in range(0, N):
        for j in range(0, N):
            if 'S' in matrix[i][j]:
                res.append((i, 'S', j))
                res_count += 1

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
