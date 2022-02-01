from random import random, getrandbits


def get_random_int(bound, number_generator=random):
    """
    Get a random integer between 0 and [bound] included.

    Parameters
    ----------
    bound : int
        Upper bound of our random positive integer.
    number_generator : callable
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). Generators that generates real numbers
    number_generator is [0,1] only
    anything else is modulo'ed by 1
    """
    return int(abs((number_generator() % 1) * (bound + 1)))

def random_int_list(n, bound, number_generator=random):
    """
    
    """
    return [get_random_int(bound, number_generator) for _ in range(n)]


def random_int_matrix(n, bound, null_diag=True, number_generator=random):
    A = [random_int_list(n, bound, number_generator) for _ in range(n)]
    if null_diag:
        for i in range(n):
            A[i][i] = 0
    return A


def random_symetric_int_matrix(n, bound, null_diag=True, number_generator=random):
    A = [[0] * n] * n
    for i in range(1, n):
        for j in range(i):
            A[i][j] = get_random_int(bound, number_generator=number_generator)
            A[j][i] = A[i][j]
    if not null_diag:
        for i in range(n):
            A[i][i] = get_random_int(bound, number_generator=number_generator)
    return A


def random_oriented_int_matrix(n, bound, null_diag=True, number_generator=random):
    A = [[0] * n] * n
    for i in range(1, n):
        for j in range(i):
            r = get_random_int(bound, number_generator=number_generator)
            if bool(getrandbits(1)):
                A[i][j] = r
            else:
                A[j][i] = r
    if not null_diag:
        for i in range(n):
            A[i][i] = get_random_int(bound, number_generator=number_generator)
    return A


def random_triangular_int_matrix(n, bound, null_diag=True, number_generator=random):
    A = [[0] * n] * n
    for j in range(n):
        for i in range(j + 1):
            A[i][j] = get_random_int(bound, number_generator=number_generator)
    if not null_diag:
        for i in range(n):
            A[i][i] = get_random_int(bound, number_generator=number_generator)
    return A
