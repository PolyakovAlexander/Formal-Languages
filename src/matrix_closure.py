def matrix_closure(matrix, grammar, N):

    for i in range(0, N):
        for j in range(0, N):
            for k in range(0, N):
                for T1 in matrix[i][j]:
                    for T2 in matrix[j][k]:
                        for (left, right) in grammar:
                            if T1 + T2 == right and left not in matrix[i][k]:
                                matrix[i][k].append(left)

    return matrix