import random
from collections import Counter


class TicTacToeAI:
    WIN_COUNT = 3

    def __init__(self):
        self.game_area = [[' ', ' ', ' '] for _ in range(3)]

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
        for row in self.game_area:
            if row.count('X') == TicTacToeAI.WIN_COUNT:
                return 'X wins'
            elif row.count('O') == TicTacToeAI.WIN_COUNT:
                return 'O wins'
            elif [row_1[0], row_2[1], row_3[2]].count('X') == TicTacToeAI.WIN_COUNT:
                return 'X wins'
            elif [row_1[0], row_2[1], row_3[2]].count('O') == TicTacToeAI.WIN_COUNT:
                return 'O wins'
            elif [row_1[2], row_2[1], row_3[0]].count('X') == TicTacToeAI.WIN_COUNT:
                return 'X wins'
            elif [row_1[2], row_2[1], row_3[0]].count('O') == TicTacToeAI.WIN_COUNT:
                return 'O wins'
            elif count[' '] == 0:
                return 'Draw'
        else:
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

    def start(self):
        # begin = input('Enter the cells: ')
        # self.game_area = [list(row.replace('_', ' ')) for row in (begin[: 3], begin[3: 6], begin[6:])]
        # print(self.game_area)
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
                    break
                print('Making move level "easy"')
                coordinates = self.rival_ai()
                mark = self.x_or_o()
                self.set_mark(coordinates, mark)
                self.render_state()
                state = self.check_state()
                if state:
                    print(state)
                    break
                continue
            else:
                print('This cell is occupied! Choose another one!')
                continue

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
Stage 2/5: Easy does it

Description

Now it's time to make a working game, so let's create our first opponent! In this version of the program, the user will be playing as X, and the computer will be playing as O at easy level.
This will be our first small step towards creating the AI!

Let's design it so that at this level the computer makes random moves. This should be perfect for people who have never played the game before!

If you want, you could make the game even simpler by including a difficulty level where the computer never wins.
Feel free to create this along with the easy level if you like, but it won't be tested.

Objectives

In this stage, you should implement the following:

Display an empty table when the program starts.
The user plays first as X, and the program should ask the user to enter cell coordinates.
Next, the computer makes its move as O, and the players then move in turn until someone wins or the game results in a draw.
Print the final outcome at the very end of the game.

Example

The example below shows how your program should work.
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

---------
|       |
|       |
|       |
---------
Enter the coordinates: > 2 2
---------
|       |
|   X   |
|       |
---------
Making move level "easy"
---------
| O     |
|   X   |
|       |
---------
Enter the coordinates: > 3 3
---------
| O     |
|   X   |
|     X |
---------
Making move level "easy"
---------
| O     |
| O X   |
|     X |
---------
Enter the coordinates: > 3 1
---------
| O     |
| O X   |
| X   X |
---------
Making move level "easy"
---------
| O     |
| O X O |
| X   X |
---------
Enter the coordinates: > 3 2
---------
| O     |
| O X O |
| X X X |
---------
X wins
"""