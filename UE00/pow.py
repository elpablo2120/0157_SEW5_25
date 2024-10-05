import time


def pow_iterativ(b, e, m):
    """
    Iterative Version von pow
    :param b: Basis
    :param e: Exponent
    :param m: Modulo
    :return: b^e mod m
    >>> pow(63, 17, 91)
    7
    >>> pow_iterativ(63, 17, 91)
    7
    """
    result = 1
    while e > 0:
        if e % 2 == 1:
            result = result * b % m
        b = b * b % m
        e = e // 2
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    a = 829287393
    b = 34938439489348938493489348939201
    n = 927492839293

    print("Pow iterativ:")
    start_time = time.time()
    print(pow_iterativ(a, b, n))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time pow_iterativ:", execution_time * 1000, "ms")

    print("\nPow:")
    start_time = time.time()
    print(pow(a, b, n))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time pow:", execution_time * 1000, "ms")