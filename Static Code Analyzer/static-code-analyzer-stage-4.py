import os
import sys
import re


class PepCheck:

    num_instances = True

    def __new__(cls):
        if cls.num_instances:
            cls.num_instances = False
            return object.__new__(cls)

    def __init__(self):
        self.counter = 0
        self.messages = {
            'S001': 'Too long',
            'S002': 'Indentation is not a multiple of four',
            'S003': 'Unnecessary semicolon',
            'S004': 'At least two spaces before inline comment required',
            'S005': 'TODO found',
            'S006': 'More than two blank lines used before this line',
            'S007': "Too many spaces after 'construction_name (def or class)'",
            'S008': "Class name 'class_name' should use CamelCase",
            'S009': "Function name 'function_name' should use snake_case"
        }
        self.check_functions = [PepCheck.check_s001, PepCheck.check_s002, PepCheck.check_s003, PepCheck.check_s004,
                                PepCheck.check_s005, PepCheck.check_s006, PepCheck.check_s007, PepCheck.check_S008,
                                PepCheck.check_S009]

    def __repr__(self):
        num_check_fun = len(self.check_functions)
        messages = '\n'.join([key + ' : ' + val for key, val in self.messages.items()])
        return f'Number of checks: {num_check_fun}\n\n{messages}'

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
        elif len(x.rstrip()) > 0 and self.counter > 2:
            self.counter = 0
            return True, 'S006'
        elif len(x.rstrip()) > 0 and self.counter <= 2:
            self.counter = 0
        return False, 'S006'

    def check_s007(self, x):
        """
        Too many spaces after construction_name (def or class)
        :param x: str
        :return: True|False, 'S007'
        """
        if 'class' in x:
            template = r'^class\s{2,}\w+'
            result = re.match(template, x.strip())
            if result:
                self.messages['S007'] = "Too many spaces after 'class'"
                return True, 'S007'
            return False, 'S007'
        if 'def' in x:
            template = r'def\s{2,}\w+'
            result = re.match(template, x.strip())
            if result:
                self.messages['S007'] = "Too many spaces after 'def'"
                return True, 'S007'
        return False, 'S007'

    def check_S008(self, x):
        """
        Class name class_name should be written in CamelCase
        :param x: str
        :return: True|False, 'S008'
        """
        if 'class' in x:
            template = r'class\s{1}[a-z_]+'
            result = re.match(template, x)
            if result:
                obj_type, c_name = result.group().split(' ')
                if not c_name.istitle():
                    self.messages['S008'] = f"Class name '{c_name}' should use CamelCase"
                    return True, 'S008'
        return False, 'S008'

    def check_S009(self, x):
        """
        Function name function_name should be written in snake_case
        :param x: str
        :return: True|False, 'S009'
        """
        if 'def' in x:
            template = r'def\s{1}[A-Z]+'
            result = re.match(template, x.strip())
            if result:
                obj_type, c_name = result.group().split(' ')
                if c_name.istitle():
                    self.messages['S009'] = f"Function name '{c_name}' should use snake_case"
                    return True, 'S009'
        return False, 'S009'

    def pep_check(self, path):
        self.counter = 0
        assert path is not str, 'path must be str object!'
        with open(path, 'r', encoding='utf-8') as code_file:
            for idx_line, line in enumerate(code_file, start=1):
                for status in self.check_functions:
                    answer = status(self, line)
                    if answer[0]:
                        print(f'{path}: Line {idx_line}: {answer[1]} {self.messages[answer[1]]}')


pep_check_inst = PepCheck()

# print(repr(pep_check_inst))

param = sys.argv[1]

if os.path.isfile(param) and param.split('.')[1] == 'py':
    pep_check_inst.pep_check(param)
elif os.path.isdir(param):
    py_files = [file for file in os.listdir(param) if '.py' in file]
    py_files.sort()
    for item in py_files:
        pep_check_inst.pep_check(os.path.join(param, item))


"""
Stage 4/5: Check names according to PEP8

Description

As many coders say, naming is one of the hardest things in programming. Good naming makes your code more readable and uniform.
Names should also follow style guides. In Python, the basic requirement is using snake_case for function names and CamelCase for class names.
Also, there should be only one space between the construction name and the object name.
Checking these rules is the next feature that we need to implement.

Check out the Python tutorial about regular expressions: they will help you implement the checks.

Objectives

In this stage, we need to add three new checks to the program:

[S007] Too many spaces after construction_name (def or class);

[S008] Class name class_name should be written in CamelCase;

[S009] Function name function_name should be written in snake_case.

Note that:

Functions names may start or end with underscores (__fun, __init__).

To simplify the task, we will assume that classes are always written as in the following examples:

# a simple class
class MyClass:
    pass

# a class based on inheritance
class MyClass(AnotherClass):
    pass
In reality, it's possible to declare a class this way:

class \
        S:
    pass
However, since it is not a common way to declare classes, you can ignore it.

Another assumption is that functions are always declared like this:

def do_magic():
    pass
As before:

The program obtains the path to the file or directory via command-line arguments:

> python code_analyzer.py directory-or-file
All the previously implemented checks should continue to work properly.

Examples
Here is an input example:

class  Person:
    pass

class user:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    @staticmethod
    def _print1():
        print('q')

    @staticmethod
    def Print2():
        print('q')
The expected output for this code is:

/path/to/file/script.py: Line 1: S007 Too many spaces after 'class'
/path/to/file/script.py: Line 4: S008 Class name 'user' should use CamelCase
/path/to/file/script.py: Line 15: S009 Function name 'Print2' should use snake_case
"""