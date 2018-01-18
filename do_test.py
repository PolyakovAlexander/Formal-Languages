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

test_data_custom = [
    ('ab.dot', 20),
    ('wwr.dot', 3),
    ('expressions.dot', 9),
    ('a-loop.dot', 16),
    ('anb.dot', 2),
    ('epsilon.dot', 6)
]


def custom_tests():
    print('Small tests...')

    for name, res in test_data_custom:
        if not test_matrix_method({name : res}, name[:-4] + '_chomsky') or \
                not test_bottom_up_method({name : res}, name[:-4]) or \
                not test_top_down_method({name : res}, name[:-4]):
            return False

    return True


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

    return True


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

    return True


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

    return True


if __name__ == '__main__':

    if custom_tests():
        print('\nAll small tests passed successfully')

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
