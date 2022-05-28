import re


class SmartCalculator:
    def __init__(self):
        self.number1 = 0
        self.number2 = 0
        self.regexp_numbers = r'-?[0-9A-z]+'
        self.regexp_symbols = r'\s[-+]+\s'
        self.memory = {}

    def normalize(self, s_lst):
        """
        Преобразуем знаки операций к нормальному виду
        :param s_lst: список, пользовательский ввод только знаки
        :return: чистый список математических операций
        """
        tmp_lst = [item.strip() for item in s_lst]
        final_lst = []
        for elem in tmp_lst:
            if '+' in elem:
                final_lst.append('+')
            elif '-' in elem:
                if len(elem) % 2 == 0:
                    final_lst.append('+')
                else:
                    final_lst.append('-')
        return final_lst

    def pipline(self, n, s):
        num_lst = n
        sym_lst = s
        for sym in sym_lst:
            num1 = num_lst.pop(0)
            num2 = num_lst.pop(0)
            if sym == '+':
                if isinstance(num1, int) and isinstance(num2, int):
                    num_lst.insert(0, num1 + num2)
                elif isinstance(num1, int) and num2.isalpha():
                    num_lst.insert(0, num1 + self.memory[num2])
                elif num1.isalpha() and isinstance(num2, int):
                    num_lst.insert(0, self.memory[num1] + num2)
                elif num1.isalpha() and num2.isalpha():
                    num_lst.insert(0, self.memory[num1] + self.memory[num2])
            elif sym == '-':
                if isinstance(num1, int) and isinstance(num2, int):
                    num_lst.insert(0, num1 - num2)
                elif isinstance(num1, int) and num2.isalpha():
                    num_lst.insert(0, num1 - self.memory[num2])
                elif num1.isalpha() and isinstance(num2, int):
                    num_lst.insert(0, self.memory[num1] - num2)
                elif num1.isalpha() and num2.isalpha():
                    num_lst.insert(0, self.memory[num1] - self.memory[num2])
        return num_lst

    def check_commands(self, command):
        if command == '/exit':
            print('Bye!')
            return True
        elif command == '/help':
            print('The program calculates the sum of numbers')
        else:
            print('Unknown command')
        return False

    def set_variable(self, line):
        message = 'Invalid assignment'
        if line.count('=') > 1:
            print(message)
            return None
        key, var = [x.strip() for x in line.split('=')]
        if not key.isalpha():
            print('Invalid identifier')
        elif key.isalpha() and var.isdigit():
            self.memory[key] = int(var)
        elif key.isalpha() and var.isalpha():
            if var in self.memory:
                self.memory[key] = self.memory[var]
            else:
                print('Unknown variable')
            return None
        else:
            print(message)
        return None

    def get_variable(self, line):
        key = line.strip()
        if key in self.memory:
            print(self.memory[key])
        else:
            print('Unknown variable')
        return None

    def start(self):
        while True:
            data = input()
            if '/' in data:
                if self.check_commands(data):
                    return
                continue
            if '=' in data:
                self.set_variable(data)
                continue
            if data.strip().isalpha():
                self.get_variable(data)
                continue
            numbers = [int(x) if not x.isalpha() else x for x in re.findall(self.regexp_numbers, data)]
            symbols = self.normalize(re.findall(self.regexp_symbols, data))
            if data.isalpha():
                print('Invalid expression')
                continue
            elif not numbers:
                if symbols:
                    print('Invalid expression')
                continue
            elif len(numbers) == 1:
                try:
                    conv = int(data)
                except ValueError:
                    print('Invalid expression')
                    continue
                print(numbers[0])
                continue
            elif not symbols:
                print('Invalid expression')
                continue
            print(self.pipline(numbers, symbols)[0])


if __name__ == '__main__':
    smart_calculator = SmartCalculator()
    smart_calculator.start()


"""
Stage 6/7: Variables

Description

In the beginning, we mentioned that the calculator will be able to store the results of previous calculations.
Do you have any idea how to do that? Of course! This can be achieved by introducing variables.
Storing results in variables and then operating on them at any time is a very convenient function.

Objectives

So, your program should support variables. Use dict to store them.

Go by the following rules for variables:

We suppose that the name of a variable (identifier) can contain only Latin letters.
A variable can have a name consisting of more than one letter.
The case is also important; for example, n is not the same as N.
The value can be an integer number or a value of another variable.
It should be possible to set a new value to an existing variable.
To print the value of a variable you should just type its name.
The example below shows how variables can be declared and displayed.

> n = 3
> m=4
> a  =   5
> b = a
> v=   7
> n =9
> count = 10
> a = 1
> a = 2
> a = 3
> a
3
Incorrect spelling or declaration of variables should also throw an exception with the corresponding message to the user:

First, the variable is checked for correctness. If the user inputs an invalid variable name, then the output should be "Invalid identifier".
> a2a
Invalid identifier
> n22
Invalid identifier
If a variable is valid but not declared yet, the program should print "Unknown variable".
> a = 8
> b = c
Unknown variable
> e
Unknown variable
If an identifier or value of a variable is invalid during variable declaration, the program must print a message like the one below.
> a1 = 8
Invalid identifier
> n1 = a2a
Invalid identifier
> n = a2a
Invalid assignment
> a = 7 = 8
Invalid assignment
Please note that the program should print "Invalid identifier" if the left part of the assignment is incorrect. If the part after the "=" is wrong then use the "Invalid assignment". First we should check the left side.

Handle as many incorrect inputs as possible. The program must never throw an exception of any kind.

It is important to note, all variables must store their values between calculations of different expressions.

Do not forget about previously implemented commands: /help and /exit.

Examples
The greater-than symbol followed by a space (>) represents the user input.

> a  =  3
> b= 4
> c =5
> a + b - c
2
> b - c + 4 - a
0
> a = 800
> a + b + c
809
> BIG = 9000
> BIG
9000
> big
Unknown variable
> /exit
Bye!
"""