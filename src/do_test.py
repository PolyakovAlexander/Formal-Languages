import os
from collections import defaultdict
from src.matrix_algo import matrix_algo as ma
from src.bottom_up_algo import bottom_up_algo as bot_up
import sys


def test(grammar_type, algo):

    src_path = os.path.abspath(os.path.dirname(__file__))
    test_data = src_path + '/data/'
    grammars_path = test_data + 'test_grammars/'
    graphs_path = test_data + 'test_graphs/'
    check_table_path = test_data + 'check_table'

    test_counter = 0
    grammars = list(filter(lambda x: grammar_type in x, os.listdir(grammars_path)))
    grammars.remove('q3_' + grammar_type)
    graphs = os.listdir(graphs_path)
    check_table = defaultdict(list)
    with open(check_table_path, 'r') as f:
        for line in f:
            graph_name, q1_res, q2_res = map(lambda x: x.replace('\n', ''), line.split(';'))
            check_table[graph_name] = [('q1_' + grammar_type, q1_res), ('q2_' + grammar_type, q2_res)]

    if algo == 'first':
        for grammar in grammars:
            for graph in graphs:
                print(grammar + ' / ' + graph + ' test: ')
                if (grammar, str(ma.matrix_algorithm(grammars_path + grammar,
                                                     graphs_path + graph, test=True))) in check_table.get(graph, []):
                    print('PASSED')
                    test_counter += 1
                else:
                    print('FAILED')
    elif algo == 'second':
        for grammar in grammars:
            for graph in graphs:
                print(grammar + ' / ' + graph + ' test: ')
                if (grammar, str(bot_up.bottom_up_algo(grammars_path + grammar,
                                                     graphs_path + graph, test=True))) in check_table.get(graph, []):
                    print('PASSED')
                    test_counter += 1
                else:
                    print('FAILED')

    print(str(test_counter) + '/' + str(len(check_table) * 2) + ' tests passed')

if __name__ == '__main__':

    test(sys.argv[1], sys.argv[2])
