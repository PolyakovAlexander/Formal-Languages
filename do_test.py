import sys
import matrix_algo
import bottom_up
import top_down

test_data_Q1 = {
    'skos.dot': 810,
    'generations.dot' : 2164,
    'travel.dot' : 2499,
    'univ-bench.dot' : 2540,
    'atom-primitive.dot' : 15454,
    'biomedical-mesure-primitive.dot' : 15156,
    'foaf.dot' : 4118,
    'people_pets.dot' : 9472,
    'funding.dot' : 17634,
    'wine.dot' : 66572,
    'pizza.dot' : 56195,
}

test_data_Q2 = {
    'skos.dot': 1,
    'generations.dot' : 0,
    'travel.dot' : 63,
    'univ-bench.dot' : 81,
    'atom-primitive.dot' : 122,
    'biomedical-mesure-primitive.dot' : 2871,
    'foaf.dot' : 10,
    'people_pets.dot' : 37,
    'funding.dot' : 1158,
    'wine.dot' : 133,
    'pizza.dot' : 1262,
}

custom_test_res = [
    (0, 'S', 1), (0, 'S', 3), (0, 'S', 5), (0, 'S', 7),
    (1, 'S', 2), (1, 'S', 4), (1, 'S', 6), (2, 'S', 3),
    (2, 'S', 5), (2, 'S', 7), (3, 'S', 4), (3, 'S', 6),
    (4, 'S', 5), (4, 'S', 7), (5, 'S', 6), (6, 'S', 7)
]


def test_matrix_method(test_data, grammar_name):
    print('\nMatrix analysis...')
    graphs_path = 'data/test_graphs/'
    grammars_path = 'data/test_grammars/'
    for name, res in test_data.items():
        print ("Test for " + grammar_name + " and " + name + " started.")
        leng = matrix_algo.matrix_algorithm(graphs_path + name, grammars_path + grammar_name, test=True)
        if leng != res:
            print (name + " failed")
            return False
        else:
            print("Test for " + grammar_name + " and " + name + " completed successfully.")


def test_bottom_up_method(test_data, grammar_name):
    print('\nBottom-up analysis...')
    graphs_path = 'data/test_graphs/'
    grammars_path = 'data/test_grammars/'
    for name, res in test_data.items():
        print("Test for " + grammar_name + " and " + name + " started.")
        leng = bottom_up.bottom_up_algo(graphs_path + name, grammars_path + grammar_name, test=True)
        if leng != res:
            print(name + " failed")
            return False
        else:
            print("Test for " + grammar_name + " and " + name + " completed successfully.")


def test_top_down_method(test_data, grammar_name):
    print('\nTop-down analysis...')
    graphs_path = 'data/test_graphs/'
    grammars_path = 'data/test_grammars/'
    for name, res in test_data.items():
        print("Test for " + grammar_name + " and " + name + " started.")
        leng = top_down.top_down(graphs_path + name, grammars_path + grammar_name, test=True)
        if leng != res:
            print (name + " failed")
            return False
        else:
            print("Test for " + grammar_name + " and " + name + " completed successfully.")


if __name__ == '__main__':

        matrix_custom = matrix_algo.matrix_algorithm('data/test_graphs/my_graph',
                                                     'data/test_grammars/my_grammar_chomsky',
                                                     custom_test=True).sort() == custom_test_res.sort()
        if matrix_custom:
            print('Custom test WWr passed with matrix algorithm on 1010101')
        else:
            print('Custom test WWr failed with matrix algorithm on 1010101')


        bottom_up_custom = bottom_up.bottom_up_algo('data/test_graphs/my_graph',
                                                    'data/test_grammars/my_grammar_automata',
                                                    custom_test=True).sort() == custom_test_res.sort()
        if bottom_up_custom:
            print('Custom test WWr passed with bottom-up algorithm on 1010101')
        else:
            print('Custom test WWr failed with bottom-up algorithm on 1010101')


        top_down_custom = top_down.top_down('data/test_graphs/my_graph',
                                            'data/test_grammars/my_grammar_automata',
                                            custom_test=True).sort() == custom_test_res.sort()
        if top_down_custom:
            print('Custom test WWr passed with top-down algorithm on 1010101')
        else:
            print('Custom test WWr failed with top-down algorithm on 1010101')

        q1_test = test_matrix_method(test_data_Q1, 'q1_chomsky')
        q2_test = test_matrix_method(test_data_Q2, 'q2_chomsky')
        if q1_test and q2_test:
            print("All tests for matrix method passed successfully")

        q1_test = test_bottom_up_method(test_data_Q1, 'q1')
        q2_test = test_bottom_up_method(test_data_Q2, 'q2')
        if q1_test and q2_test:
            print("All tests for bottom-up method passed successfully")

        q1_test = test_top_down_method(test_data_Q1, 'q1')
        q2_test = test_top_down_method(test_data_Q2, 'q2')
        if q1_test and q2_test:
            print("All tests for top-down method passed successfully")
