import sys
import utils
import gll_classes


def top_down(graph_path, gram_path, out=None, test=False, custom_test=False):

    automaton = utils.parse_graph(graph_path, gll=True)
    grammar, _ = utils.parse_grammar(gram_path)
    gll = gll_classes.GLL(grammar, automaton)

    res = gll.main()
    custom_res = []
    res_count = 0
    for i, nonterm, j in res:
        if nonterm == 'S':
            res_count += 1

    if test:
        return res_count
    elif out is None:
        if custom_test:
            for i, nonterm, j in res:
                if nonterm == 'S':
                    custom_res.append((i, nonterm, j))
            return custom_res
        else:
            for i, nonterm, j in res:
                print(i, nonterm, j)
    else:
        with open(out, 'w') as f:
            for i, nonterm, j in res:
                f.write(str(i) + ',' + nonterm + ',' + str(j) + '\n')

if __name__ == '__main__':

    if len(sys.argv) == 4:
        top_down(sys.argv[1], sys.argv[2], out=sys.argv[3])
    elif len(sys.argv) == 3:
        top_down(sys.argv[1], sys.argv[2])
    else:
        print('Incorrect amount of arguments, run script like this: '
              'python3 bottom_up.py [automaton] [grammar] [output]')
