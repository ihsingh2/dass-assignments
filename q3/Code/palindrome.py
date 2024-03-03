"""Module for palindrome_days."""

def palindrome_days(year: int) -> str:
    """Returns palindrome days for a given year, when one exists.

    Args:
        year: An integer between 0 and 9999.

    Returns:
        A DD-MM-YYYY palindromic string when possible, a failure
        message otherwise.

    Raises:
        ValueError: year argument is not an integer, or is out of range.
    """

    if not isinstance(year, int):
        raise ValueError('Argument should be an integer.')

    if not 0 <= year <= 9999:
        raise ValueError('Argument should be between 0 and 9999.')

    failure_msg = 'No Palindrome days available in the given year'

    yearstr = f'{year:04}'
    daystr = yearstr[-1:-3:-1]
    monthstr = yearstr[-3::-1]

    day = int(daystr)
    month = int(monthstr)

    if not 1 <= month <= 12:
        return failure_msg

    if month in (1, 3, 5, 7, 8, 10, 12):
        if not 1 <= day <= 31:
            return failure_msg
    elif month != 2:
        if not 1 <= day <= 30:
            return failure_msg
    else:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if not 1 <= day <= 29:
                return failure_msg
        else:
            if not 1 <= day <= 28:
                return failure_msg

    return f'{daystr}-{monthstr}-{yearstr}'

if __name__ == '__main__':
    arg = input('Enter a year smaller than 9999: ')
    if arg.isnumeric():
        print(palindrome_days(int(arg)))
    else:
        print('Argument should be a non-negative integer.')
