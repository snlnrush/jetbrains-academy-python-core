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

    def start(self):
        while True:
            data = input()
            if data == '/exit':
                print('Bye!')
                return
            if data == '/help':
                print('The program calculates the sum of numbers')
                continue
            numbers = data.split()
            if not numbers:
                continue
            if len(numbers) == 1:
                print(numbers[0])
                continue
            numbers = list(map(int, re.findall(self.regexp_numbers, data)))
            symbols = self.normalize(re.findall(self.regexp_symbols, data))
            print(self.pipline(numbers, symbols)[0])


if __name__ == '__main__':
    smart_calculator = SmartCalculator()
    smart_calculator.start()


"""
Stage 4/7: Add subtractions

Description

Finally, we got to the next operation: subtraction. It means that from now on the program must receive the addition + and subtraction - operators as an input to distinguish operations from each other.
It must support both unary and binary minus operators. Moreover, If the user has entered several same operators following each other, the program still should work (like Java or Python REPL).
Also, as you remember from school math, two adjacent minus signs turn into a plus. The smart calculator ought to have such a feature.

Pay attention to the /help command, it is important to maintain its relevance depending on the changes (in the next stages too).
You can write information about your program in free form, but the main thing is that it should be understandable to you and other users.

Objectives

The program must calculate expressions like these: 4 + 6 - 8, 2 - 3 - 4, and so on.
Modify the result of the /help command to explain these operations.
Decompose your program using functions to make it easy to understand and edit later.
The program should not stop until the user enters the /exit command.
If you encounter an empty line, do not output anything.
Examples
The greater-than symbol followed by a space (>) represents the user input.

> 8
8
> -2 + 4 - 5 + 6
3
> 9 +++ 10 -- 8
27
> 3 --- 5
-2
> 14       -   12
2
> /exit
Bye!
"""