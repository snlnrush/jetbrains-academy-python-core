import re


class SmartCalculator:
    def __init__(self):
        self.number1 = 0
        self.number2 = 0
        self.regexp_numbers = r'-?[0-9]+'
        self.regexp_symbols = r'\s[-+]+\s'

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
                num_lst.insert(0, num1 + num2)
            elif sym == '-':
                num_lst.insert(0, num1 - num2)
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

    def start(self):
        while True:
            data = input()
            if '/' in data:
                if self.check_commands(data):
                    return
                continue
            numbers = list(map(int, re.findall(self.regexp_numbers, data)))
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
Stage 5/7: Error_

Description

Now you need to consider the reaction of the calculator when users enter expressions in the wrong format.
The program only knows numbers, a plus sign, a minus sign, and two commands. It cannot accept all other characters and it is necessary to warn the user about this.

Objectives
The program should print Invalid expression in cases when the given expression has an invalid format. If a user enters an invalid command, the program must print Unknown command.
All messages must be printed without quotes. The program must never throw an exception.
To handle incorrect input, you should remember that the user input that starts with / is a command, in other situations, it is an expression.

Do not forget to write methods to decompose your program.

Like before, /help command should print information about your program. When the command /exit is entered, the program must print Bye! , and then stop.

Examples

The greater-than symbol followed by a space (>) represents the user input.

> 8 + 7 - 4
11
> abc
Invalid expression
> 123+
Invalid expression
> +15
15
> 18 22
Invalid expression
>
> -22
-22
> 22-
Invalid expression
> /go
Unknown command
> /exit
Bye!
"""