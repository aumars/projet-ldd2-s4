from random import (random,
                    getrandbits,
                    sample)


def get_random_int(bound, number_generator=random):
    """
    Get a random integer between 0 and [bound] included.

    Parameters
    ----------
    bound : int
        Upper bound of our random positive integer.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    int
        Random integer between 0 and [bound] included.

    Raises
    ------
    ValueError
        If [bound] is not positive.
    """
    if not (bound >= 0):
        raise ValueError("bound={} must be positive."
                         .format(bound))
    else:
        return int((number_generator() % 1) * (bound + 1))


def random_int_list(n, bound, number_generator=random):
    """
    Generate a list of length [n] containing random integers between 0 and
    [bound] included.

    Parameters
    ----------
    n : int
        Length of list. Must be positive.
    bound : int
        Upper bound of our random positive integers. Must be positive if [n] is
        non zero.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    list int
        List of length [n] containing random integers between 0 and [bound]
        included.

    Raises
    ------
    ValueError
        If [n] is not positive.
    """
    if not (n >= 0):
        raise ValueError("n={} must be positive."
                         .format(n))
    else:
        return [get_random_int(bound, number_generator) for _ in range(n)]


def random_int_matrix(n, bound, null_diag=True, number_generator=random):
    """
    Generate a square matrix of size [n] * [n] containing random integers
    between 0 and [bound] included.

    Parameters
    ----------
    n : int
        Height/width of square matrix. Must be positive.
    bound : int
        Upper bound of our random positive integers. Must be positive if [n] is
        non zero.
    null_diag : bool, optional
        Flag to make the diagonal of the square matrix to only contain zeros.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    list list int
        Square matrix of size [n] * [n] containing random integers between 0
        and [bound] included.

    Raises
    ------
    ValueError
        If [n] is not positive.
    """
    if not (n >= 0):
        raise ValueError("n={} must be positive."
                         .format(n))
    else:
        A = [random_int_list(n, bound, number_generator) for _ in range(n)]
        if null_diag:
            for i in range(n):
                A[i][i] = 0
        return A


def random_symetric_int_matrix(n, bound, null_diag=True,
                               number_generator=random):
    """
    Generate a symetric square matrix of size [n] * [n] containing random
    integers between 0 and [bound] included, where each element a_ij equals
    a_ji.

    Parameters
    ----------
    n : int
        Height/width of square matrix. Must be positive.
    bound : int
        Upper bound of our random positive integers. Must be positive if [n] is
        non zero.
    null_diag : bool, optional
        Flag to make the diagonal of the square matrix to only contain zeros.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    list list int
        Symetric square matrix of size [n] * [n] containing random integers
        between 0 and [bound] included.

    Raises
    ------
    ValueError
        If [n] is not positive.
    ValueError
        If [bound] is strictly negative and [n] is strictly positive.
    """
    if not (n >= 0):
        raise ValueError("n={} must be positive."
                         .format(n))
    elif bound < 0 and n > 0:
        raise ValueError("bound={} must be positive."
                         .format(bound))
    else:
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            for j in range(i):
                A[i][j] = get_random_int(bound,
                                         number_generator=number_generator)
                A[j][i] = A[i][j]
        if not null_diag:
            for i in range(n):
                A[i][i] = get_random_int(bound,
                                         number_generator=number_generator)
        return A


def random_oriented_int_matrix(n, bound, null_diag=True,
                               number_generator=random):
    """
    Generate a square matrix of size [n] * [n] containing random integers
    between 0 and [bound] included, where each element a_ij has its symetric
    a_ji to equal 0.

    Parameters
    ----------
    n : int
        Height/width of square matrix. Must be positive.
    bound : int
        Upper bound of our random positive integers. Must be positive if [n] is
        non zero.
    null_diag : bool, optional
        Flag to make the diagonal of the square matrix to only contain zeros.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    list list int
        Square matrix of size [n] * [n] containing random integers between 0
        and [bound] included.

    Raises
    ------
    ValueError
        If [n] is not positive.
    """
    if not (n >= 0):
        raise ValueError("n={} must be positive."
                         .format(n))
    else:
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            for j in range(i):
                r = get_random_int(bound, number_generator=number_generator)
                if bool(getrandbits(1)):
                    A[i][j] = r
                else:
                    A[j][i] = r
        if not null_diag:
            for i in range(n):
                A[i][i] = get_random_int(bound,
                                         number_generator=number_generator)
        return A


def random_triangular_int_matrix(n, bound, null_diag=True,
                                 number_generator=random):
    """
    Generate a triangular matrix of size [n] * [n] containing random integers
    between 0 and [bound] included.

    Parameters
    ----------
    n : int
        Height/width of triangular matrix. Must be positive.
    bound : int
        Upper bound of our random positive integers. Must be positive if [n] is
        non zero.
    null_diag : bool, optional
        Flag to make the diagonal of the triangular matrix to only contain
        zeros.
    number_generator : callable, optional
        Random number generator that generates real numbers between 0 and 1
        (included or excluded). If [number_generator] generates real
        positive numbers, only the non-integer part is kept.

    Returns
    -------
    list list int
        Triangular matrix of size [n] * [n] containing random integers between
        0 and [bound] included.

    Raises
    ------
    ValueError
        If [n] is not positive.
    ValueError
        If [bound] is strictly negative and [n] is strictly positive.
    """
    if not (n >= 0):
        raise ValueError("n={} must be positive."
                         .format(n))
    elif bound < 0 and n > 0:
        raise ValueError("bound={} must be positive."
                         .format(bound))
    else:
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            for j in range(i):
                A[i][j] = get_random_int(bound,
                                         number_generator=number_generator)
        if not null_diag:
            for i in range(n):
                A[i][i] = get_random_int(bound,
                                         number_generator=number_generator)
        return A
