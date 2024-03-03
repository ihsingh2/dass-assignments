"""Module for unit tests on palindrome_days."""

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../Code'))

import pytest
from palindrome import palindrome_days

def test_non_integer_input():
    """Tests handling of non string input."""

    with pytest.raises(ValueError, match='^Argument should be an integer.$'):
        palindrome_days(16.2)
    with pytest.raises(ValueError, match='^Argument should be an integer.$'):
        palindrome_days('2012')

def test_out_of_bound_input():
    """Tests handling of out of bound input."""

    with pytest.raises(ValueError, match='^Argument should be between 0 and 9999.$'):
        palindrome_days(-1)
    with pytest.raises(ValueError, match='^Argument should be between 0 and 9999.$'):
        palindrome_days(10000)
    with pytest.raises(ValueError, match='^Argument should be between 0 and 9999.$'):
        palindrome_days(-100000)
    with pytest.raises(ValueError, match='^Argument should be between 0 and 9999.$'):
        palindrome_days(100000)

def test_invalid_months():
    """Tests failure when the reverse of first two digits does not constitute a month."""

    failure_msg = 'No Palindrome days available in the given year'
    assert palindrome_days(3111) == failure_msg
    assert palindrome_days(1211) == failure_msg
    assert palindrome_days(1511) == failure_msg
    assert palindrome_days(7811) == failure_msg

def test_invalid_days():
    """Tests failure when the reverse of last two digits does not constitute a day."""

    failure_msg = 'No Palindrome days available in the given year'
    assert palindrome_days(2100) == failure_msg
    assert palindrome_days(2123) == failure_msg
    assert palindrome_days(2176) == failure_msg
    assert palindrome_days(2148) == failure_msg

def test_validity_combination():
    """Tests validity of days for a given month and year."""

    failure_msg = 'No Palindrome days available in the given year'
    assert palindrome_days(2003) == failure_msg
    assert palindrome_days(4013) == failure_msg
    assert palindrome_days(8013) != failure_msg
    assert palindrome_days(2113) != failure_msg
    assert palindrome_days(2092) != failure_msg

def test_success_output():
    """Tests the correctness of output when no failure of error is expected."""

    assert palindrome_days(2170) == '07-12-2170'
    assert palindrome_days(3013) == '31-03-3013'
    assert palindrome_days(5042) == '24-05-5042'
    assert palindrome_days(7051) == '15-07-7051'
    assert palindrome_days(9020) == '02-09-9020'
