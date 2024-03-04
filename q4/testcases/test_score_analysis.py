"""Module for unit tests on score_analysis."""

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../Code'))

import pytest
from score_analysis import calculate_average, find_highest_scorer, process_dataset

def test_average_bad_input():
    """Tests handling of bad input in calculate_average."""

    with pytest.raises(ValueError):
        bad_input = [
            {'name': 'abcd', 'marks': [25.0]},
            {'name': 'efgh', 'marks': [50.0]},
            {'name': 'ijkl', 'marks': [75.0]},
            {'name': 'mnop', 'marks': [100.0]},
        ]
        calculate_average(bad_input)

def test_average_degenerate_input():
    """Tests handling of degenerate input in calculate_average."""

    assert calculate_average(None) == {}
    assert calculate_average([]) == {}

def test_average_single_score():
    """Tests output of calculate_average on list of students with score of single subject."""

    test_input = [
        {'name': 'abcd', 'scores': [25.0]},
        {'name': 'efgh', 'scores': [50.0]},
        {'name': 'ijkl', 'scores': [75.0]},
        {'name': 'mnop', 'scores': [100.0]},
    ]

    expected_output = {
        'abcd': 25.0,
        'efgh': 50.0,
        'ijkl': 75.0,
        'mnop': 100.0,
    }

    assert calculate_average(test_input) == expected_output

def test_average_multiple_scores():
    """Tests output of calculate_average on list of students with multiple subjects."""

    test_input = [
        {'name': 'wczvjkx', 'scores': [10.0, 70.0, 46.0, 46.0, 14.0]},
        {'name': 'dmurtmdg', 'scores': [58.0, 74.0, 17.0, 62.0, 21.0]},
        {'name': 'ynbzryi', 'scores': [62.0, 41.0, 49.0, 98.0, 87.0]},
        {'name': 'clenvx', 'scores': [82.0, 28.0, 41.0, 24.0, 23.0]},
        {'name': 'gdcvvd', 'scores': [11.0, 53.0, 42.0, 71.0, 87.0]},
        {'name': 'ilhmwzkli', 'scores': [66.0, 63.0, 89.0, 46.0, 2.0]},
        {'name': 'gkbcjins', 'scores': [42.0, 65.0, 6.0, 79.0, 6.0]},
        {'name': 'mvxvxxr', 'scores': [36.0, 88.0, 59.0, 35.0, 55.0]}
    ]

    expected_output = {
        'wczvjkx': 37.20,
        'dmurtmdg': 46.40,
        'ynbzryi': 67.40,
        'clenvx': 39.60,
        'gdcvvd': 52.80,
        'ilhmwzkli': 53.20,
        'gkbcjins': 39.60,
        'mvxvxxr': 54.60
    }

    assert calculate_average(test_input) == expected_output

def test_highest_score_bad_input():
    """Tests handling of bad input in find_highest_scorer."""

    with pytest.raises(ValueError):
        unrecognised_key = [
            {'name': 'abcd', 'marks': [25.0]},
            {'name': 'efgh', 'marks': [50.0]},
            {'name': 'ijkl', 'marks': [75.0]},
            {'name': 'mnop', 'marks': [100.0]},
        ]
        find_highest_scorer(unrecognised_key)

    with pytest.raises(ValueError):
        inconsistent_subjects = [
            {'name': 'abcd', 'scores': [25.0, 50.0]},
            {'name': 'efgh', 'scores': [50.0]},
            {'name': 'ijkl', 'scores': [75.0]},
            {'name': 'mnop', 'scores': [100.0]},
        ]
        find_highest_scorer(inconsistent_subjects)

def test_highest_score_degenerate_input():
    """Tests handling of degenerate input in find_highest_scorer."""

    no_subjects = [
        {'name': 'abcd', 'scores': []},
        {'name': 'efgh', 'scores': []},
        {'name': 'ijkl', 'scores': []},
        {'name': 'mnop', 'scores': []},
    ]

    assert find_highest_scorer(None) == ('', [])
    assert find_highest_scorer([]) == ('', [])
    assert find_highest_scorer(no_subjects) == ('', [])

def test_highest_score_single_score():
    """Tests output of find_highest_scorer on list of students with score of single subject."""

    test_input = [
        {'name': 'abcd', 'scores': [25.0]},
        {'name': 'efgh', 'scores': [50.0]},
        {'name': 'ijkl', 'scores': [75.0]},
        {'name': 'mnop', 'scores': [100.0]},
    ]

    expected_output = (
        'mnop',
        ['mnop']
    )

    assert find_highest_scorer(test_input) == expected_output

def test_highest_score_multiple_scores():
    """Tests output of find_highest_scorer on list of students with multiple subjects."""

    test_input = [
        {'name': 'wczvjkx', 'scores': [10.0, 70.0, 46.0, 46.0, 14.0]},
        {'name': 'dmurtmdg', 'scores': [58.0, 74.0, 17.0, 62.0, 21.0]},
        {'name': 'ynbzryi', 'scores': [62.0, 41.0, 49.0, 98.0, 87.0]},
        {'name': 'clenvx', 'scores': [82.0, 28.0, 41.0, 24.0, 23.0]},
        {'name': 'gdcvvd', 'scores': [11.0, 53.0, 42.0, 71.0, 87.0]},
        {'name': 'ilhmwzkli', 'scores': [66.0, 63.0, 89.0, 46.0, 2.0]},
        {'name': 'gkbcjins', 'scores': [42.0, 65.0, 6.0, 79.0, 6.0]},
        {'name': 'mvxvxxr', 'scores': [36.0, 88.0, 59.0, 35.0, 55.0]}
    ]

    expected_output = (
        'ynbzryi',
        ['clenvx', 'mvxvxxr', 'ilhmwzkli', 'ynbzryi', 'gdcvvd']
    )

    assert find_highest_scorer(test_input) == expected_output

def test_process_dataset_wrong_path():
    """Tests handling of wrong path in process_dataset."""

    with pytest.raises(FileNotFoundError):
        process_dataset('do_not_create_this_file.txt')

def test_process_dataset_non_numeric_input():
    """Tests handling of non numeric input in process_dataset."""

    with pytest.raises(ValueError):
        process_dataset('Dataset/bad_input_1.txt')

def test_process_valid_input():
    """Tests handling of valid input in process_dataset."""

    expected_output = [
        {'name': 'wczvjkx', 'scores': [10.0, 70.0, 46.0, 46.0, 14.0]},
        {'name': 'dmurtmdg', 'scores': [58.0, 74.0, 17.0, 62.0, 21.0]},
        {'name': 'ynbzryi', 'scores': [62.0, 41.0, 49.0, 98.0, 87.0]},
        {'name': 'clenvx', 'scores': [82.0, 28.0, 41.0, 24.0, 23.0]},
        {'name': 'gdcvvd', 'scores': [11.0, 53.0, 42.0, 71.0, 87.0]},
        {'name': 'ilhmwzkli', 'scores': [66.0, 63.0, 89.0, 46.0, 2.0]},
        {'name': 'gkbcjins', 'scores': [42.0, 65.0, 6.0, 79.0, 6.0]},
        {'name': 'mvxvxxr', 'scores': [36.0, 88.0, 59.0, 35.0, 55.0]}
    ]

    output = process_dataset('Dataset/data1.txt')
    assert output == expected_output
