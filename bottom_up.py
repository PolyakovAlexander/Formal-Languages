import utils
import sys


# Transitive closure
def closure(matrix, size, map_indices,
            start_states, final_states,
            automaton, active_edges):

    changes = False
    is_changing = True
    while is_changing:
        is_changing = False
        for i, j in active_edges:
            for k in range(size):
                if matrix[j][k] and not matrix[i][k]:

                    # add new way
                    matrix[i][k] = True
                    is_changing = True
                    a, b = map_indices[i]
                    c, d = map_indices[k]

                    # update automaton
                    if b in start_states.keys() and d in final_states.keys() \
                            and (a, c, start_states[b]) not in automaton:
                        automaton.append((a, c, start_states[b]))

        if is_changing:
            changes = True

    return matrix, automaton, changes


# Grammar(RFA) and automaton(FSM) intersection
def intersection(indices, automaton,
                 grammar, matrix, final_states,
                 start_states, active_edges):

    changes = False
    is_changing = True
    while is_changing:
        is_changing = False
        for a, b, c in grammar:
            for x, y, z in automaton:
                if z == c:
                    i = indices[(int(x), int(a))]
                    j = indices[(int(y), int(b))]

                    # update results matrix
                    if not matrix[i][j]:
                        matrix[i][j] = True
                        active_edges.add((i, j))
                        is_changing = True

                    # update automaton
                    if a in start_states.keys() and b in final_states.keys() \
                            and (x, y, start_states[a]) not in automaton:
                        automaton.append((x, y, start_states[a]))
                        is_changing = True

        if is_changing:
            changes = True

    return matrix, automaton, active_edges , changes


def bottom_up_algo(automaton_path, grammar_path, out=None, test=False):

    # grammar parameters
    g, grammar_vertex = utils.parse_grammar(grammar_path)
    grammar = g.edges
    start_states = g.starts
    final_states = g.finals
    n = g.length

    # RFA parameters
    automaton, k, automaton_vertex = utils.parse_graph(automaton_path)

    matrix = [[False for i in range(n * k)] for j in range(n * k)]

    # set of edges used in transitive closure
    active_edges = set()

    # allows to work with (i, j) coordinates instead of (0, 0'), (1, 1')
    map_indices_to_states = dict()

    counter = 0
    for a in automaton_vertex:
        for b in grammar_vertex:
            map_indices_to_states[counter] = (int(a), int(b))
            counter += 1

    indices = {v: k for k, v in map_indices_to_states.items()}

    res = set()

    for st_state, st_nterm in start_states.items():
        for fin_state, fin_nterm in final_states.items():
            if st_nterm == fin_nterm and fin_state == st_state:
                for i in automaton_vertex:
                    res.add((str(i) + ',' + fin_nterm + ',' + str(i) + '\n').replace(' ', ''))

    smth_changes = True
    while smth_changes:

        smth_changes = False
        matrix, automaton, active_edges, inters_change = intersection(indices, automaton,
                                                        grammar, matrix,
                                                        final_states, start_states,
                                                        active_edges)

        matrix, automaton, closure_change = closure(matrix, n * k,
                                                    map_indices_to_states,
                                                    start_states, final_states,
                                                    automaton, active_edges)
        if inters_change or closure_change:
            smth_changes = True

    for i in range(n * k):
        for j in range(n * k):
            if matrix[i][j]:
                a, b = map_indices_to_states[i]
                c, d = map_indices_to_states[j]
                if b in start_states.keys() and d in final_states.keys():
                    res.add(str(a) + ',' + start_states[b] + ',' + str(c) + '\n')

    test_res = [x for x in res if ',S,' in x]

    if test:
        return len(test_res)
    elif out is None:
        for item in res:
            print(item.strip())
    else:
        with open(out, 'w') as f:
            for item in res:
                f.write(item)

if __name__ == '__main__':

    if len(sys.argv) == 4:
        bottom_up_algo(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        bottom_up_algo(sys.argv[1], sys.argv[2])
    else:
        print('Incorrect amount of arguments, run script like this: '
              'python3 bottom_up.py [automaton] [grammar]  [output]')