import os
import sys


class PepCheck:

    def __init__(self):
        self.counter = 0
        self.messages = {
            'S001': 'Too long',
            'S002': 'Indentation is not a multiple of four',
            'S003': 'Unnecessary semicolon',
            'S004': 'At least two spaces before inline comment required',
            'S005': 'TODO found',
            'S006': 'More than two blank lines used before this line'
        }
        self.check_functions = [PepCheck.check_s001, PepCheck.check_s002, PepCheck.check_s003, PepCheck.check_s004,
                                PepCheck.check_s005, PepCheck.check_s006]

    def check_s001(self, x):
        return len(x.rstrip()) > 79, 'S001'

    def check_s002(self, x):
        return (len(x) - len(x.lstrip(' '))) % 4 != 0, 'S002'

    def check_s003(self, x):
        if ';' in x:
            return ');' in x.rstrip() or 's;' in x.rstrip(), 'S003'
        else:
            return False, 'S003'

    def check_s004(self, x):
        return not x.startswith('#') and '#' in x and not x.split('#')[0].endswith('  '), 'S004'

    def check_s005(self, x):
        if '#' in x and 'todo' in x.lower():
            split_lst = x.split('#')
            return 'todo' in split_lst[1].lower(), 'S005'
        else:
            return False, 'S005'

    def check_s006(self, x):
        assert x is not str, 'Must be str object!'
        if len(x.rstrip()) == 0:
            self.counter += 1
        if len(x.rstrip()) > 0 and self.counter > 2:
            self.counter = 0
            return True, 'S006'
        return False, 'S006'

    def pep_check(self, path):
        self.counter = 0
        assert path is not str, 'path must be str object!'
        with open(path, 'r', encoding='utf-8') as code_file:
            for idx_line, line in enumerate(code_file, start=1):
                for status in self.check_functions:
                    answer = status(self, line)
                    if answer[0]:
                        print(f'{path}: Line {idx_line}: {answer[1]} {self.messages[answer[1]]}')


param = sys.argv[1]

pep_check_inst = PepCheck()

if os.path.isfile(param) and param.split('.')[1] == 'py':
    pep_check_inst.pep_check(param)
elif os.path.isdir(param):
    py_files = [file for file in os.listdir(param) if '.py' in file]
    py_files.sort()
    for item in py_files:
        pep_check_inst.pep_check(os.path.join(param, item))

"""
Stage 3/5: Analyze multi-file projects

Description

As a rule, real projects contain more than a single file. Also, project directories often contain not only Python files, and we don't need to check if an HTML file follows PEP8.

We recommend that you check out a tutorial on realpython.com that can help you to work with files and directories.

Objectives
In this stage, you need to improve your program so that it can analyze all Python files inside a specified directory.

Please note that:

You also need to change the input format. Instead of reading the path from the standard input, the program must obtain it as a command-line argument:

> python code_analyzer.py directory-or-file
The output format also needs to be changed slightly. It should include the path to the analyzed file:

Path: Line X: Code Message 
All output lines must be sorted in ascending order according to the file name, line number, and issue code.

Non-Python files must be skipped.

Once again:

It is important that all the checks implemented in the previous stages continue to work properly.

If a line contains the same stylistic issue several times, your program must print the information only once. If a line has several issues with different types of error codes, they should be printed in ascending order.

To simplify the solution, we consider it acceptable if your program finds some false-positive stylistic issues in strings, especially in multi-lines ('''...''' and """...""").

We recommend that you break your program code into a set of functions and classes to avoid confusion.

Examples

Only a single file is specified as the input:

> python code_analyzer.py /path/to/file/script.py
/path/to/file/script.py: Line 1: S004 At least two spaces required before inline comments
/path/to/file/script.py: Line 2: S003 Unnecessary semicolon
/path/to/file/script.py: Line 3: S001 Too long line
/path/to/file/script.py: Line 3: S003 Unnecessary semicolon
/path/to/file/script.py: Line 6: S001 Too long line
/path/to/file/script.py: Line 11: S006 More than two blank lines used before this line
/path/to/file/script.py: Line 13: S003 Unnecessary semicolon
/path/to/file/script.py: Line 13: S004 At least two spaces required before inline comments
/path/to/file/script.py: Line 13: S005 TODO found
The input path is a directory; the output should contain all Python files from it:

> python code_analyzer.py /path/to/project
/path/to/project/__init__.py: Line 1: S001 Too long line
/path/to/project/script1.py: Line 1: S004 At least two spaces required before inline comments
/path/to/project/script1.py: Line 2: S003 Unnecessary semicolon
/path/to/project/script2.py: Line 1: S004 At least two spaces required before inline comments
/path/to/project/script2.py: Line 3: S001 Too long line
/path/to/project/somedir/script.py: Line 3: S001 Too long line
/path/to/project/test.py: Line 3: Line 13: S003 Unnecessary semicolon
"""