## Question 1A - Kaooa

- Initial: 0.00/10
- Lint 1: 4.42/10
  - Revision: Change indentation from 2 spaces, to 4 spaces.
- Lint 2: 4.88/10
  - Revision: Remove trailing whitespaces.
- Lint 3: 4.48/10
  - Revision: Split long lines into multiple statements (the drop is due to refactoring of methods in some cases).
- Lint 4: 6.44/10
  - Revision: Declare no argument methods as class methods.
- Lint 5: 8.11/10
  - Revision:
    1. Conform to snake_case naming style for attributes, arguments and variables.
    2. Conform to UPPER_CASE naming style for constants.
    3. Vary variable names in chains of function calls.
    4. Fix issues with conditional returns, and comparision with None.
    5. Fix argument inconsistency in method overriding, attribute definitions, and import order.
- Lint 6: 9.09/10
  - Revision: Add docstrings.
- Final: 10.00/10
  - Revision: Fix pygame related issues.

## Question 1B - Lucas

- Initial: 7.69/10
- Lint 1: 9.23/10
  - Revision: Renamed variable 'next' to 'succ', and 'L_num' to 'L_NUM'.
  - Pending: Change module name 'Lucas_1' to snake_case.

## Question 2 - Kaprekar's Routine

- Steps to run the program

```console
cd q2/
python Code/kaprekarroutine.py
{Enter a four-digit number with at least two different digits:} 1122
```

- Steps to run the testcases

```console
cd q2/
python testcases/test_kaprekarroutine.py
```

- Test cases covered: Non string input, non numeric input, negative input, floating point input, short input, long input, recurring digit input, output type check, inclusion of input and Kaprekar's constant in output, trivial single iteration termination, 5 or less iterations terminations, more than 5 iteration termination. 

## Question 3 - Palindrome

- Steps to run the program

```console
cd q3/
python Code/palindrome.py
{Enter a year smaller than 9999:} 152
```

- Steps to run the testcases

```console
cd q3/
pytest testcases/test_palindrome.py
```

- Test cases covered: Non integer input, out of bound input, invalid months, invalid days, invalid combinations, randomly sampled successful outputs.

## Question 4 - Student Scores

- Steps to run the program

```console
cd q4/
python Code/score_analysis.py
{Enter the input path:} Dataset/data1.txt
```

- Steps to generate random datasets

```console
cd q4/
python Dataset/generate_dataset.py
{Enter the output path:} Dataset/new.txt
```

- Testcases are expected to be run from ``q4/`` directory, for the sake of relative file path.

```console
cd q4/
pytest testcases/test_score_analysis.py
```

- Test cases covered: Bad input, degenerate input, trivial input, non-trivial input.
