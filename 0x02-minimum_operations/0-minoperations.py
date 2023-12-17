#!/usr/bin/python3
""" Minimum Operations """


def minOperations(n: object) -> object:
    """ method that calculates the fewest number of operations needed
    @param n:
    @return:
    """
    if n <= 1:
        return 0
    count = 0
    for i in range(2, n + 1):
        while n % i == 0:
            count += i
            n = n / i
    return count
