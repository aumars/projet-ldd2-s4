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


def gray_code(n):
    """
    Generate the gray code with n bits.

    Parameters
    ----------
    n : int
        The numbers of bits.

    Returns
    -------
    list str
        The ordering list of gray code with n bits.

    Raises
    ------
    ValueError
        If bit_string is not composed of bit.
    """
    def int2bin(n, k):
        bin_compressed = bin(n)[2:]
        return (k - len(bin_compressed)) * "0" + bin_compressed

    gray = []
    for k in range(2 ** n):
        gray.append(int2bin(k ^ (k >> 1), n))
    if gray == ['0']:
        return ['']
    else:
        return gray


def K_map(bit_string):
    """
    Generate the Karnaugh table.

    Parameters
    ----------
    bit_string : string
        A bit string of the truth table output.

    Returns
    -------
    list list int
        The Karnaugh table.

    Raises
    ------
    ValueError
        If bit_string is not composed of bit.
    """
    not_pow2 = f"bit_string = {bit_string} is not a power of 2."
    for c in bit_string:
        if c != '0' and c != '1':
            raise ValueError(f"bit_string = {bit_string} is not entirely composed of bits.")
    if bin(len(bit_string))[2] == '0' and len(bit_string) > 3:
        raise ValueError(not_pow2)
    for c in bin(len(bit_string))[3:]:
        if c == '1':
            raise ValueError(not_pow2)
    n = len(bin(len(bit_string))) - 3
    K = [[None for _ in range(n)] for _ in range(n)]
    for k in range(n**2):
        gray = k ^ (k >> 1)
        i, j = k // n, k % n
        K[i][j] = int(bit_string[gray])
    for i in range(1, n, 2):
        K[i].reverse()
    return K


def bit_string_to_formula(bit_string):
    """
    Generate the formula from a bit string.

    Parameters
    ----------
    bit_string : string
        A bit string of the truth table output.    
    
    Returns
    -------
    string
        The formula thats corresponds to the bit string.

    Raises
    ------
    ValueError
        If bit_string is not composed of bit.
    """
    
def adder(self, r1, r2, hold_bit):
    """
    Cumpute the sum of the regiter r1 and r2.
    
    Parameters
    ----------
    r1 : int list
        The first registre. The length must be a power of 2.

    r2 : int list
        The second registre. The length must be a power of 2.

    hold_bit : int
        A hold bit.

    Returns
    -------
    int list
        The sum of registres.
    int 
        A carry bit. Set to 1 if the calculation has exceeded the size of the
        register. Otherwise set to 0.

    Raises
    ------
    ValueError
        If the length of the argument r1 or r2 is not a power of 2.
    """ 
    pass

def half_adder(self, r1, r2):
    """
    Cumpute the sum of the regiter r1 and r2.
    
    Parameters
    ----------
    r1 : int list
        The first registre. The length must be a power of 2.

    r2 : int list
        The second registre. The length must be a power of 2.

    Returns
    -------
    int list
        The sum of registres.
    int 
        A carry bit. Set to 1 if the calculation has exceeded the size of the
        register. Otherwise set to 0.

    Raises
    ------
    ValueError
        If the length of the argument r1 or r2 is not a power of 2.
    """ 
    pass