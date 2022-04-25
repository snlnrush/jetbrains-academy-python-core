import os
import sys
import re
import ast


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
            'S009': "Function name 'function_name' should use snake_case",
            'S010': "Argument name arg_name should be written in snake_case",
            'S011': "Variable var_name should be written in snake_case",
            'S012': "The default argument value is mutable"
        }
        self.check_functions = [PepCheck.check_s001, PepCheck.check_s002, PepCheck.check_s003, PepCheck.check_s004,
                                PepCheck.check_s005, PepCheck.check_s006, PepCheck.check_s007, PepCheck.check_s008,
                                PepCheck.check_s009]

    def __repr__(self):
        num_check_fun = len(self.check_functions)
        messages = '\n'.join([key + ' : ' + val for key, val in self.messages.items()])
        return f'Number of checks: {num_check_fun}\n\n{messages}'

    @staticmethod
    def check_s001(self, x):
        return len(x.rstrip()) > 79, 'S001'

    @staticmethod
    def check_s002(self, x):
        return (len(x) - len(x.lstrip(' '))) % 4 != 0, 'S002'

    @staticmethod
    def check_s003(self, x):
        if ';' in x:
            return ');' in x.rstrip() or 's;' in x.rstrip(), 'S003'
        else:
            return False, 'S003'

    @staticmethod
    def check_s004(self, x):
        return not x.startswith('#') and '#' in x and not x.split('#')[0].endswith('  '), 'S004'

    @staticmethod
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

    def check_s008(self, x):
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

    def check_s009(self, x):
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

    @staticmethod
    def check_s010(x, path):
        """
        Argument name arg_name should be written in snake_case
        :param x: str, file.py object
        :param path: str, path to file
        :return: True|False, 'S010'
        """
        tree = ast.parse(x)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = [a.arg for a in node.args.args]
                for arg in function_name:
                    if arg.isupper() or arg.istitle() and arg != 'self':
                        print(f"{path}: Line {node.lineno}: S010 Function name '{arg}' should use snake_case")
        return False, 'S010'

    @staticmethod
    def check_s011(x, path):
        """
        Default argument value is mutable
        :param x: str, file.py object
        :param path: str, path to file
        :return: True|False, 'S011'
        """
        tree = ast.parse(x)
        for row, node in enumerate(ast.walk(tree), start=1):
            if isinstance(node, ast.FunctionDef):
                for node2 in node.body:
                    if isinstance(node2, ast.Assign):
                        for node3 in node2.targets:
                            if isinstance(node3, ast.Name):
                                def_var = node3.id
                                if def_var.isupper() or def_var.istitle():
                                    print(f"{path}: Line {node3.lineno}: S011 Variable '{def_var}' "
                                          f"in function should be snake_case")
        return False, 'S011'

    @staticmethod
    def check_s012(x, path):
        """
        Default argument value is mutable
        :param x: str, file.py object
        :param path: str, path to file
        :return: True|False, 'S012'
        """
        tree = ast.parse(x)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for value in node.args.defaults:
                    if isinstance(value, ast.List):
                        print(f"{path}: Line {node.lineno}: S012 Default argument value is mutable")
        return False, 'S012'

    def pep_check(self, path):
        self.counter = 0
        assert path is not str, 'path must be str object!'
        with open(path, 'r', encoding='utf-8') as code_file:
            data_code = []
            for idx_line, line in enumerate(code_file, start=1):
                data_code.append(line)
                for status in self.check_functions:
                    answer = status(self, line)
                    if answer[0]:
                        print(f'{path}: Line {idx_line}: {answer[1]} {self.messages[answer[1]]}')
            pack_data_code = ''.join(data_code)
            for status in [PepCheck.check_s010, PepCheck.check_s011, PepCheck.check_s012]:
                status(pack_data_code, path)


pep_check_inst = PepCheck()

param = sys.argv[1]

if os.path.isfile(param) and param.split('.')[1] == 'py':
    pep_check_inst.pep_check(param)
elif os.path.isdir(param):
    py_files = [file for file in os.listdir(param) if '.py' in file]
    py_files.sort()
    for item in py_files:
        pep_check_inst.pep_check(os.path.join(param, item))


"""
Stage 5/5: Analyze arguments and variables

Description

In this final stage, you need to improve your program to check that all the names of function arguments as well as local variables meet the requirements of PEP8. The program must not force the names of variables outside of functions (for example, in modules or classes). The most convenient way to do this is to use the Abstract Syntactic Tree (AST) from the ast module.

Also, your program must check that the given code does not use mutable values (lists, dictionaries, and sets) as default arguments to avoid errors in the program.

Objectives

You need to add three new checks to your analyzer:

[S010] Argument name arg_name should be written in snake_case;

[S011] Variable var_name should be written in snake_case;

[S012] The default argument value is mutable.

Please note that:

Names of functions, as well as names of variables in the body of a function should be written in snake_case. However, the error message for an invalid function name should be output only when the function is defined. The error message for an invalid variable name should be output only when this variable is assigned a value, not when this variable is used further in the code.

To simplify the task, you only need to check whether the mutable value is directly assigned to an argument:

def fun1(test=[]):  # default argument value is mutable
    pass


def fun2(test=get_value()):  # you can skip this case to simplify the problem
    pass
If a function contains several mutable arguments, the message should be output only once for this function.

Variable and argument names are assumed to be valid if they are written in snake_case. Initial underscores (_) are also acceptable.

As before:

You can use other messages, but the check codes must be exactly as given above.

All the previously implemented checks should continue to work correctly, and the program should be able to read from one or more files.

Examples
Here is an input example:

CONSTANT = 10
names = ['John', 'Lora', 'Paul']


def fun1(S=5, test=[]):  # default argument value is mutable
    VARIABLE = 10
    string = 'string'
    print(VARIABLE)
The expected output for this code is:

/path/to/file/script.py: Line 5: S010 Argument name 'S' should be snake_case
/path/to/file/script.py: Line 5: S012 Default argument value is mutable
/path/to/file/script.py: Line 6: S011 Variable 'VARIABLE' in function should be snake_case
Note that the message for the line print(VARIABLE) is not printed since it was already output for line 6, where the variable VARIABLE is assigned a value.
"""