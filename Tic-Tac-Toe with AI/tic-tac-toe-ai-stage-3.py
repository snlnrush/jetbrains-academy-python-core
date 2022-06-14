import random
from collections import Counter


class TicTacToeAI:
    WIN_COUNT = 3
    GAME_SIZE = 3

    def __init__(self):
        self.game_area = self.gen_game_area()

    def gen_game_area(self):
        return [[' ', ' ', ' '] for _ in range(TicTacToeAI.GAME_SIZE)]

    def input_data(self):
        while True:
            try:
                coordinates = [int(x) for x in input('Enter the coordinates: ').split(' ')]
            except ValueError:
                print('You should enter numbers!')
                continue
            for coord in coordinates:
                if coord > 3:
                    print('Coordinates should be from 1 to 3!')
                    break
            else:
                return coordinates

    def is_empty(self, coordinates):
        row, column = coordinates
        return self.game_area[row - 1][column - 1] == ' '

    def set_mark(self, coordinates, mark):
        row, column = coordinates
        self.game_area[row - 1][column - 1] = mark
        return None

    def x_or_o(self):
        row_1, row_2, row_3 = self.game_area
        count = Counter(''.join(row_1) + ''.join(row_2) + ''.join(row_3))
        if count['X'] > count['O']:
            return 'O'
        else:
            return 'X'

    def check_state(self):
        row_1, row_2, row_3 = self.game_area
        count = Counter(''.join(row_1) + ''.join(row_2) + ''.join(row_3))
        for idx in range(TicTacToeAI.GAME_SIZE):
            column = [row[idx] for row in self.game_area]
            if column.count('X') == TicTacToeAI.WIN_COUNT:
                return 'X wins'
            elif column.count('O') == TicTacToeAI.WIN_COUNT:
                return 'O wins'
        for row in self.game_area:
            if row.count('X') == TicTacToeAI.WIN_COUNT:
                return 'X wins'
            elif row.count('O') == TicTacToeAI.WIN_COUNT:
                return 'O wins'
        if [row_1[0], row_2[1], row_3[2]].count('X') == TicTacToeAI.WIN_COUNT:
            return 'X wins'
        elif [row_1[0], row_2[1], row_3[2]].count('O') == TicTacToeAI.WIN_COUNT:
            return 'O wins'
        elif [row_1[2], row_2[1], row_3[0]].count('X') == TicTacToeAI.WIN_COUNT:
            return 'X wins'
        elif [row_1[2], row_2[1], row_3[0]].count('O') == TicTacToeAI.WIN_COUNT:
            return 'O wins'
        elif count[' '] == 0:
            return 'Draw'
        return False

    def rival_ai(self):
        empty_field_coordinates = []
        for row in range(3):
            for col in range(3):
                if self.is_empty((row, col)):
                    empty_field_coordinates.append((row, col))
        random.shuffle(empty_field_coordinates)
        move_rival_coordinates = empty_field_coordinates[0]
        return move_rival_coordinates

    def user_vs_ai(self):
        self.render_state()
        while True:
            coordinates = self.input_data()
            if self.is_empty(coordinates):
                mark = self.x_or_o()
                self.set_mark(coordinates, mark)
                self.render_state()
                state = self.check_state()
                if state:
                    print(state)
                    return None
                print('Making move level "easy"')
                coordinates = self.rival_ai()
                mark = self.x_or_o()
                self.set_mark(coordinates, mark)
                self.render_state()
                state = self.check_state()
                if state:
                    print(state)
                    return None
                continue
            else:
                print('This cell is occupied! Choose another one!')
                continue

    def ai_vs_user(self):
        self.render_state()
        while True:
            print('Making move level "easy"')
            coordinates = self.rival_ai()
            mark = self.x_or_o()
            self.set_mark(coordinates, mark)
            self.render_state()
            state = self.check_state()
            if state:
                print(state)
                return None
            coordinates = self.input_data()
            if self.is_empty(coordinates):
                mark = self.x_or_o()
                self.set_mark(coordinates, mark)
                self.render_state()
                state = self.check_state()
                if state:
                    print(state)
                    return None
                continue
            else:
                print('This cell is occupied! Choose another one!')
                continue

    def ai_vs_ai(self):
        self.render_state()
        while True:
            print('Making move level "easy"')
            coordinates = self.rival_ai()
            mark = self.x_or_o()
            self.set_mark(coordinates, mark)
            self.render_state()
            state = self.check_state()
            if state:
                print(state)
                return None

    def user_vs_user(self):
        self.render_state()
        while True:
            coordinates = self.input_data()
            if self.is_empty(coordinates):
                mark = self.x_or_o()
                self.set_mark(coordinates, mark)
                self.render_state()
                state = self.check_state()
                if state:
                    print(state)
                    return None
                continue
            else:
                print('This cell is occupied! Choose another one!')
                continue

    def start(self):
        while True:
            command = input('Input command: ').split(' ')
            if len(command) == 1 and command[0] == 'exit':
                break
            elif len(command) != 3 or command[0] != 'start':
                print('Bad parameters!')
                continue
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'easy':
                self.ai_vs_ai()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'user':
                self.ai_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'easy':
                self.user_vs_ai()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'user':
                self.user_vs_user()
            self.game_area = self.gen_game_area()
            print()

    def render_state(self):
        line_border = '---------'
        print(line_border)
        for row in self.game_area:
            print('|', ' '.join(row), '|')
        print(line_border)


def main():
    tictactoe_ai = TicTacToeAI()
    tictactoe_ai.start()


if __name__ == '__main__':
    main()


"""
Stage 3/5: Watch 'em fight

Description

It's time to make things more interesting by adding some game variations.
What if you want to play against a friend instead of the AI? How about if you get tired of playing the game and want to see a match between two AIs?
You also need to give the user the option of going first or second when playing against the AI.

It should be possible for the user to quit the game after the result is displayed as well.

Objectives

Your tasks for this stage are:

Write a menu loop, which can interpret two commands: start and exit.
Implement the command start. It should take two parameters: who will play X and who will play O. Two options are possible for now: user to play as a human, and easy to play as an AI.
The exit command should simply end the program.
In later steps, you will add the medium and hard levels.

Don't forget to handle incorrect input! The message Bad parameters! should be displayed if what the user enters is invalid.

Example

The example below shows how your program should work.
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Input command: > start
Bad parameters!
Input command: > start easy
Bad parameters!
Input command: > start easy easy
---------
|       |
|       |
|       |
---------
Making move level "easy"
---------
|       |
|     X |
|       |
---------
Making move level "easy"
---------
|       |
| O   X |
|       |
---------
Making move level "easy"
---------
|       |
| O   X |
|     X |
---------
Making move level "easy"
---------
|       |
| O   X |
|   O X |
---------
Making move level "easy"
---------
|       |
| O X X |
|   O X |
---------
Making move level "easy"
---------
|     O |
| O X X |
|   O X |
---------
Making move level "easy"
---------
| X   O |
| O X X |
|   O X |
---------
X wins

Input command: > start easy user
---------
|       |
|       |
|       |
---------
Making move level "easy"
---------
|       |
|       |
|     X |
---------
Enter the coordinates: > 2 2
---------
|       |
|   O   |
|     X |
---------
Making move level "easy"
---------
|   X   |
|   O   |
|     X |
---------
Enter the coordinates: > 3 1
---------
|   X   |
|   O   |
| O   X |
---------
Making move level "easy"
---------
|   X X |
|   O   |
| O   X |
---------
Enter the coordinates: > 2 3
---------
|   X X |
|   O O |
| O   X |
---------
Making move level "easy"
---------
| X X X |
|   O O |
| O   X |
---------
X wins

Input command: > start user user
---------
|       |
|       |
|       |
---------
Enter the coordinates: > 3 1
---------
|       |
|       |
| X     |
---------
Enter the coordinates: > 2 2
---------
|       |
|   O   |
| X     |
---------
Enter the coordinates: > 2 1
---------
|       |
| X O   |
| X     |
---------
Enter the coordinates: > 3 2
---------
|       |
| X O   |
| X O   |
---------
Enter the coordinates: > 1 1
---------
| X     |
| X O   |
| X O   |
---------
X wins

Input command: > exit
"""