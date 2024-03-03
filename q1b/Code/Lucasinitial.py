"""
Module for printing an element of the series L_n, given by
L_n = L_{n-1} + L_{n-2} , n > 1
    = -1                , n = 1
    = -3                , n = 0
"""

def compute_series_at(index: int):
    """
    Returns the value of the series at the index argument.
    """

    if index < 0:
        raise ValueError('Index should be a non-negative integer.')

    curr, next = -3, -1
    for _ in range(index):
        curr, next = next, curr + next

    return curr

arg = input('Enter the value of n: ')
if arg.isnumeric():
    num = int(arg)
else:
    raise ValueError("Index should be a non-negative integer.")

L_num = compute_series_at(index = int(arg))
print(f'L_n = {L_num}')
