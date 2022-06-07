import sys
import re


class Conversion:
    def __init__(self, expression):
        self.expression = expression
        self.top = -1
        self.array = []
        self.output = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def isEmpty(self):
        return True if self.top == -1 else False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return False

    def push(self, op):
        self.top += 1
        self.array.append(op)

    def isOperand(self, ch):
        return ch.isnumeric()

    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self):
        for i in self.expression:
            if self.isOperand(i):
                self.output.append(i)
            elif i == '(':
                self.push(i)
            elif i == ')':
                while ((not self.isEmpty()) and
                       self.peek() != '('):
                    self.output.append(self.pop())
                if not self.isEmpty() and self.peek() != '(':
                    return -1
                else:
                    self.pop()
            else:
                while not self.isEmpty() and self.notGreater(i):
                    self.output.append(self.pop())
                self.push(i)
        while not self.isEmpty():
            self.output.append(self.pop())
        return self.output


class Evaluate:
    def __init__(self, expression):
        self.top = -1
        self.expression = expression
        self.array = []

    def isEmpty(self):
        return True if self.top == -1 else False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return '$'

    def push(self, op):
        self.top += 1
        self.array.append(op)

    def evaluatePostfix(self):
        for i in self.expression:
            if i.isdigit():
                self.push(i)
            else:
                val1 = self.pop()
                val2 = self.pop()
                self.push(str(eval(val2 + i + val1)))
        return int(float(self.pop()))


class Calculator:
    def __init__(self):
        self.variable_dictionary = {}

    @staticmethod
    def balanced_brackets(inp):
        pairs = {"(": ")"}
        stack = []
        for i in inp:
            if i in "(":
                stack.append(i)
            elif stack and i == pairs[stack[-1]]:
                stack.pop()
            elif not stack and i == ")":
                return False
            else:
                continue
        return len(stack) == 0

    def parse_user_input(self):
        user_input = input()
        replacements = [('[+]{2,}', '+'), ('[*]{2,}', 'Invalid expression'), ('[/]{2,}', 'Invalid expression'),
                        ('[-]{3,}', '-'), ('[-]{2,}', '+')]
        for old, new in replacements:
            user_input = re.sub(old, new, user_input)
            if 'Invalid expression' in user_input:
                print('Invalid expression')
                user_input = []
                input_type = 'wrong input'
                return user_input, input_type
        if user_input.startswith('/'):
            user_input = user_input.split()
            input_type = 'command'
        elif user_input.strip().isalpha():
            user_input = user_input.strip().split()
            input_type = 'call_variable'
        elif user_input.strip().isnumeric() or user_input.lstrip('-').strip().isnumeric():
            print(user_input.strip())
            user_input = []
            input_type = 'print_digit'
        elif '=' in user_input:
            user_input = [i.strip() for i in user_input.split('=') if i != '']
            input_type = 'variable_declaration'
        else:
            user_input = (' ' + i + ' ' if not i.isalnum() else i for i in user_input)
            user_input = [i for i in ''.join(user_input).split(' ') if i != '']
            if not self.balanced_brackets(user_input):
                print('Invalid expression')
                user_input = []
                input_type = 'wrong input'
                return user_input, input_type
            else:
                try:
                    user_input = [i if not i.isalpha() else str(self.variable_dictionary[i])
                                  for i in user_input]
                except KeyError:
                        print('Unknown variable')
                        user_input = []
            input_type = 'expression'

        return user_input, input_type

    @staticmethod
    def validate_identifier(user_input, printing=True):
        validate = user_input.isalpha()
        if not validate and printing:
            print('Invalid identifier')
        return validate

    @staticmethod
    def validate_assignment_general(user_input):
        validate = re.match(r'(^[0-9]+$)', user_input) or re.match(r'(^[a-zA-Z]+$)', user_input)
        if not validate:
            print('Invalid assignment')
        return validate

    @staticmethod
    def validate_assignment_number(user_input):
        validate = user_input.isnumeric()
        return validate

    @staticmethod
    def validate_assignment_letter(user_input):
        validate = user_input.isalpha()
        return validate

    def build_variable_dictionary(self, user_input):
        if not self.validate_identifier(user_input[0]):
            return False
        if not self.validate_assignment_general(user_input[1]):
            return False
        if self.validate_identifier(user_input[0], printing=False) and self.validate_assignment_number(user_input[1]):
            self.variable_dictionary[user_input[0]] = int(user_input[1])
        if self.validate_identifier(user_input[0], printing=False) and self.validate_assignment_letter(user_input[1]):
            if user_input[1] in self.variable_dictionary:
                self.variable_dictionary[user_input[0]] = self.variable_dictionary[user_input[1]]
            else:
                print('Unknown variable')

    def return_variable_value(self, user_input, printing=False):
        if user_input in self.variable_dictionary:
            if printing:
                print(self.variable_dictionary[user_input])
                return self.variable_dictionary[user_input]
            else:
                return self.variable_dictionary[user_input]
        else:
            print('Unknown variable')

    def run_input(self):
        user_input, input_type = self.parse_user_input()
        if len(user_input) == 0:
            user_input_to_calc = False
        elif input_type == 'command' and user_input[0] not in ('/exit', '/help'):
            print('Unknown command')
            user_input_to_calc = False
        elif user_input[0] == '/exit':
            print('Bye!')
            sys.exit()
        elif user_input[0] == '/help':
            print('The program calculates  the addition, multiplication, subtraction and division - operations')
            user_input_to_calc = False
        elif input_type == 'call_variable':
            user_input_to_calc = False
            validation = self.validate_identifier(user_input[0])
            if validation:
                self.return_variable_value(user_input[0], printing=True)
        elif input_type == 'variable_declaration' and len(user_input) > 2:
            print('Invalid assignment')
            user_input_to_calc = False
        elif input_type == 'variable_declaration' and len(user_input) == 2:
            self.build_variable_dictionary(user_input)
            user_input_to_calc = False
        else:
            user_input_to_calc = True

        return user_input_to_calc, user_input

    def calculate(self):
        while True:
            user_input_to_calc, user_input = self.run_input()
            if user_input_to_calc:
                result = Evaluate(Conversion(user_input).infixToPostfix()).evaluatePostfix()
                print(result)
            else:
                continue


if __name__ == '__main__':
    Calculator().calculate()


"""
Stage 7/7: I’ve got the power
Description
In the final stage, it remains to add operations: multiplication *, integer division / and parentheses (...). They have a higher priority than addition + and subtraction -.

Here is an example of an expression that contains all possible operations:

3 + 8 * ((4 + 3) * 2 + 1) - 6 / (2 + 1)
The result is 121.

A general expression can contain many parentheses and operations with different priorities. It is difficult to calculate such expressions if you do not use special methods. Fortunately, there is a fairly effective and universal solution, using a stack, to calculate the most general expressions.

From infix to postfix

Earlier we processed expressions written in infix notation. This notation is not very convenient if an expression has operations with different priorities, especially when brackets are used. But we can use postfix notation, also known as Reverse Polish notation (RPN). In this notation, operators follow their operands. See several examples below.

Infix notation 1:

3 + 2 * 4
Postfix notation 1:

3 2 4 * +
Infix notation 2:

2 * (3 + 4) + 1
Postfix notation 2:

2 3 4 + * 1 +
To better understand the postfix notation, you can play with a converter.

As you can see, in postfix notation operations are arranged according to their priority and parentheses are not used at all. So, it is easier to calculate expressions written in postfix notation.

You can use a stack (LIFO) to convert an expression from infix to postfix notation. The stack is used to store operators for reordering. Here are some rules that describe how to create an algorithm that converts an expression from infix to postfix notation.

Add operands (numbers and variables) to the result (postfix notation) as they arrive.
If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
If the incoming operator has higher precedence than the top of the stack, push it on the stack.
If the precedence of the incoming operator is lower than or equal to that of the top of the stack, pop the stack and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the top of the stack; then add the incoming operator to the stack.
If the incoming element is a left parenthesis, push it on the stack.
If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. Discard the pair of parentheses.
At the end of the expression, pop the stack and add all operators to the result.
No parentheses should remain on the stack. Otherwise, the expression has unbalanced brackets. It is a syntax error.

Calculating the result

When we have an expression in postfix notation, we can calculate it using another stack. To do that, scan the postfix expression from left to right:

If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
If the incoming element is the name of a variable, push its value into the stack.
If the incoming element is an operator, then pop twice to get two numbers and perform the operation; push the result on the stack.
When the expression ends, the number on the top of the stack is a final result.
Here you can find an example and additional explanations on postfix expressions.

Objectives
Your program should support multiplication *, integer division / and parentheses (...). To do this, use infix to postfix conversion algorithm above and then calculate the result using stack.
Do not forget about variables; they, and the unary minus operator, should still work.
Modify the result of the /help command to explain all possible operators. You can write the output for the command in free form.
The program should not stop until the user enters the /exit command.
Note that a sequence of + (like +++ or +++++) is an admissible operator that should be interpreted as a single plus. A sequence of - (like -- or ---) is also an admissible operator and its meaning depends on the length. If a user enters a sequence of * or /, the program must print a message that the expression is invalid.
As a bonus, you may add the power operator ^ that has a higher priority than * and /.
> 2^2
4
> 2*2^3
16
Examples
The greater-than symbol followed by a space (>) represents the user input.

> 8 * 3 + 12 * (4 - 2)
48
> 2 - 2 + 3
3
> 4 * (2 + 3
Invalid expression
> -10
-10
> a=4
> b=5
> c=6
> a*2+b*3+c*(2+3)
53
> 1 +++ 2 * 3 -- 4
11
> 3 *** 5
Invalid expression
> 4+3)
Invalid expression
> /command
Unknown command
> /exit
Bye!
"""