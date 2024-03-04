"""Module for generating datasets for score_analysis"""

import random
import string

def generate_random_string(length: int):
    """Generates a random lowercase alphabet string of the given length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

if __name__ == '__main__':
    filename = input('Enter the output path: ')
    num_records = random.randrange(5, 15)
    num_values = random.randrange(3, 6)

    with open(filename, "w") as f:
        for _ in range(num_records):
            string_length = random.randrange(5, 10)
            random_string = generate_random_string(string_length)
            for _ in range(num_values):
                random_string += ', ' + str(random.randrange(1, 101))
            random_string += '\n'
            f.write(random_string)

    print(f'Generated {num_records} records of {num_values} values.')
