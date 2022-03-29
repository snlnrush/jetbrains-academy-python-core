def check_s001(x):
    return len(x.rstrip()) > 79, 'S001'


def check_s002(x):
    return (len(x) - len(x.lstrip(' '))) % 4 != 0, 'S002'


def check_s003(x):
    if ';' in x:
        return ');' in x.rstrip() or 's;' in x.rstrip(), 'S003'
    else:
        return False, 'S003'


def check_s004(x):
    return not x.startswith('#') and '#' in x and not x.split('#')[0].endswith('  '), 'S004'


def check_s005(x):
    if '#' in x and 'todo' in x.lower():
        split_lst = x.split('#')
        return 'todo' in split_lst[1].lower(), 'S005'
    else:
        return False, 'S005'


def check_s006(x):
    assert x is not str, 'Must be str object!'
    global COUNTER
    if len(x.rstrip()) == 0:
        COUNTER += 1
    if len(x.rstrip()) > 0 and COUNTER > 2:
        COUNTER = 0
        return True, 'S006'
    return False, 'S006'


COUNTER = 0

check_functions = [check_s001, check_s002, check_s003, check_s004, check_s005, check_s006]

messages = {
            'S001': 'Too long',
            'S002': 'Indentation is not a multiple of four',
            'S003': 'Unnecessary semicolon',
            'S004': 'At least two spaces before inline comment required',
            'S005': 'TODO found',
            'S006': 'More than two blank lines used before this line'
            }

path = input()

with open(path, 'r', encoding='utf-8') as code_file:
    for idx_line, line in enumerate(code_file, start=1):
        for status in check_functions:
            answer = status(line)
            if answer[0]:
                print(f'Line {idx_line}: {answer[1]} {messages[answer[1]]}')

"""
Stage 2/5: New checks

Description

Let's add a few more checks to the program. All of them are consistent with the PEP8 style guide.

Objectives

In this stage, you need to add checks for the following five errors to your program:

[S002] Indentation is not a multiple of four;

[S003] Unnecessary semicolon after a statement (note that semicolons are acceptable in comments);

[S004] Less than two spaces before inline comments;

[S005] TODO found (in comments only and case-insensitive);

[S006] More than two blank lines preceding a code line (applies to the first non-empty line).

Please note that:

If a line contains the same stylistic issue several times, your program should print the information only once. However, if a single line has several issues with different types of error codes, they should be printed as a sorted list.

To simplify the task, we consider it acceptable if your program finds some false-positive stylistic issues in strings, especially in multi-lines ('''...''' and """...""").

We recommend that you break your code into a set of functions to avoid confusion.

Once again:

The path to the file with Python code is obtained from standard input.

The general output format is:

Line X: Code Message
The lines with found issues must be output in ascending order.
Examples
Here is an example of badly styled Python code (please never write code like this!):

print('What\'s your name?') # reading an input
name = input();
print(f'Hello, {name}');  # here is an obvious comment: this prints a greeting with a name


very_big_number = 11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
print(very_big_number)



def some_fun():
    print('NO TODO HERE;;')
    pass; # Todo something
It contains nine code style issues:

Line 1: S004 At least two spaces required before inline comments
Line 2: S003 Unnecessary semicolon
Line 3: S001 Too long
Line 3: S003 Unnecessary semicolon
Line 6: S001 Too long
Line 11: S006 More than two blank lines used before this line
Line 13: S003 Unnecessary semicolon
Line 13: S004 At least two spaces required before inline comments
Line 13: S005 TODO found
"""