def matrix_closure(matrix, grammar, N):

    for i in range(N):
        for j in range(N):
            for k in range(N):
                for T1 in matrix[i][j]:
                    for T2 in matrix[j][k]:
                        for left, right in grammar.items():
                            for value in right:
                                if T1 + ' ' + T2 == value and left not in matrix[i][k]:
                                    matrix[i][k].append(left)

    return matrix