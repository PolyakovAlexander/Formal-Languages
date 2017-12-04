import os
from collections import defaultdict
import matrix_algo as ma

src_path = os.path.abspath(os.path.dirname(__file__))
test_data = src_path + '/../data/'
grammars_path = test_data + 'test_grammars/'
graphs_path = test_data + 'test_graphs/'
check_table_path = test_data + 'check_table'

test_counter = 0
grammars = os.listdir(grammars_path)
graphs = os.listdir(graphs_path)
check_table = defaultdict(list)
with open(check_table_path, 'r') as f:
    for line in f:
        graph_name, q1_res, q2_res = map(lambda x: x.replace('\n', ''), line.split(';'))
        check_table[graph_name] = [('q1_grammar', q1_res), ('q2_grammar', q2_res)]

for grammar in grammars:
    for graph in graphs:
        if (grammar, str(ma.matrix_algorithm(grammars_path + grammar,
                                             graphs_path + graph, test=True))) in check_table.get(graph, []):
            print(grammar + ' / ' + graph + ' test: PASSED')
            test_counter += 1
        else:
            print(grammar + ' / ' + graph + ' test: FAILED')

print(str(test_counter) + '/' + str(len(check_table) * 2) + ' tests passed')