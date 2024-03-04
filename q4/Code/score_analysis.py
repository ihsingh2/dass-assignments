"""Module for score analysis of students."""

def calculate_average(students: list) -> dict:
    """
    Takes a list of student dictionaries and returns a dictionary
    of student names with their average scores.

    Args:
        A list of students dictionaries with key 'name' and value
        'scores', which is a list of integers.

    Returns:
        A new dictionary of student names, with values equal to
        the average of their 'scores' in the argument list.
    """

    if students is None or len(students) == 0:
        return {}

    averages = {}
    for student in students:
        try:
            if len(student['scores']) > 0:
                averages[student['name']] = sum(student['scores']) / len(student['scores'])
            else:
                averages[student['name']] = 0
        except Exception as exc:
            raise ValueError('Unable to parse the input.') from exc
    return averages

def find_highest_scorer(students: list) -> (str, list):
    """
    Takes a list of student dictionaries and returns the name of the
    student with highest average score, the ordered list of students
    who scored highest in individual subjects.

    Args:
        A list of students dictionaries with key 'name' and value
        'scores', which is a list of integers.

    Returns:
        Name of the student with highest average score across subjects,
        and the ordered list of student names who scored highest in
        individual subjects. Ties, if any, are broken by comparision
        of name string, and list index as last resort.

    Raises:
        ValueError: List of scores are of inconsistent length,
        for different students,
    """

    if students is None or len(students) == 0:
        return '', []

    try:
        num_subjects = len(students[0]['scores'])
        for student in students:
            if num_subjects != len(student['scores']):
                raise ValueError('All students are expected to have the same number of subjects.')
    except Exception as exc:
        raise ValueError('Unable to parse the input.') from exc

    if num_subjects == 0:
        return '', []

    highest_scores = [ students[0]['scores'][i] for i in range(num_subjects) ]
    highest_scorers = [ students[0]['name'] for _ in range(num_subjects) ]

    for student in students:
        name = student['name']
        for subject in range(num_subjects):
            score = student['scores'][subject]
            if highest_scores[subject] < score:
                highest_scores[subject] = score
                highest_scorers[subject] = name
            elif highest_scores[subject] == score:
                highest_scorers[subject] = min(highest_scorers[subject], name)

    averages = calculate_average(students)
    highest_avg_scorer = students[0]['name']
    highest_avg_score = averages[highest_avg_scorer]

    for name, avg_score in averages.items():
        if highest_avg_score < avg_score:
            highest_avg_score = avg_score
            highest_avg_scorer = name
        elif highest_avg_score == avg_score:
            highest_avg_scorer = min(highest_avg_scorer, name)

    return highest_avg_scorer, highest_scorers

def process_dataset(input_path: str) -> list:
    """
    Reads an input file with lines consisting of comma-separated values.

    Args:
        The path to the input file.

    Returns:
        A list of dictionaries of name and scores value, corresponding
        to the first and remaining values, for each line.

    Raises:
        FileNotFoundError: Failure in opening the file.
        ValueError: Non-first values are not numeric.
    """

    dataset = []
    try:
        file = open(input_path, "r")
    except Exception as exc:
        raise FileNotFoundError('Unable to access the file.') from exc

    for line in file:
        values = line.strip().split(',')
        if len(values) == 0:
            break

        name = values[0]
        try:
            scores = [ float(x) for x in values[1:] ]
        except Exception as exc:
            raise ValueError('Expected numeric arguments.') from exc
        dataset.append({'name': name, 'scores': scores})

    file.close()
    return dataset

if __name__ == '__main__':
    file_path = input('Enter the input path: ')
    input_dictionary = process_dataset(file_path)

    student_averages = calculate_average(input_dictionary)
    highest_average_scorer, highest_subject_scorer = find_highest_scorer(input_dictionary)

    print('\nAverage Scores:')
    for student_name, average_score in student_averages.items():
        print(f'{student_name}: {average_score:.2f}')
    print()

    print(f'Student with highest average: {highest_average_scorer}')
    print(f'Highest scores in each subject: {highest_subject_scorer}')
