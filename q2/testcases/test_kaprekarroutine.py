"""Module for unit tests on kaprekar_routine."""

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../Code'))

import unittest
from kaprekarroutine import kaprekar_routine

class TestKaprekarRoutine(unittest.TestCase):
    """Unit test suite for the function kaprekar_routine. """

    def test_non_string_input(self):
        """Tests handling of non string input."""
        with self.assertRaises(ValueError):
            kaprekar_routine(1234)

    def test_non_numeric_input(self):
        """Tests handling of non-numeric string input."""
        with self.assertRaises(ValueError):
            kaprekar_routine('abcd')

    def test_negative_input(self):
        """Tests handling of negative input."""
        with self.assertRaises(ValueError):
            kaprekar_routine('-987')
        with self.assertRaises(ValueError):
            kaprekar_routine('-9876')

    def test_floating_point_input(self):
        """Tests handling of floating point input."""
        with self.assertRaises(ValueError):
            kaprekar_routine('98.7')
        with self.assertRaises(ValueError):
            kaprekar_routine('98.76')

    def test_short_input(self):
        """Tests handling of strings of length less than 4."""
        with self.assertRaises(ValueError):
            kaprekar_routine('123')

    def test_long_input(self):
        """Tests handling of strings of length more than 4."""
        with self.assertRaises(ValueError):
            kaprekar_routine('12345')

    def test_recurring_digit_input(self):
        """Tests handling of strings with no two distinct digits."""
        with self.assertRaises(ValueError):
            kaprekar_routine('1111')

    def test_single_iteration_input(self):
        """Tests Kaprekar's routine on the trivial single iteration case."""
        output = kaprekar_routine('6174')
        self.assertEqual(output, '6174')

    def test_less_iterations_input(self):
        """Tests Kaprekar's routine on input that terminate in five or less iterations."""

        cases = [
            ('1234', '1234, 3087, 8352, 6174'),
            ('1678', '1678, 7083, 8352, 6174'),
            ('4862', '4862, 6174'),
            ('8567', '8567, 3087, 8352, 6174'),
            ('9357', '9357, 6174')
        ]

        for input, expected_output in cases:
            output = kaprekar_routine(input)
            self.assertEqual(output, expected_output)
        
    def test_more_iterations_input(self):
        """Tests Kaprekar's routine on input that terminate in more than five iterations."""

        cases = [
            ('1038', '1038, 8172, 7443, 3996, 6264, 4176, 6174'),
            ('3186', '3186, 7263, 5265, 3996, 6264, 4176, 6174'),
            ('4789', '4789, 5085, 7992, 7173, 6354, 3087, 8352, 6174'),
            ('8319', '8319, 8442, 5994, 5355, 1998, 8082, 8532, 6174'),
            ('9610', '9610, 9441, 7992, 7173, 6354, 3087, 8352, 6174')
        ]

        for input, expected_output in cases:
            output = kaprekar_routine(input)
            self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
