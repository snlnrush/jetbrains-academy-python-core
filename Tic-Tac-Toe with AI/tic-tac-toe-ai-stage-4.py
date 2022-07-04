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
                # coordinates = [int(x) for x in input('Enter the coordinates: ').split(' ')]
                coordinates = [int(x) - 1 for x in input('Enter the coordinates: ').split(' ')]
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
        # return self.game_area[row - 1][column - 1] == ' '
        return self.game_area[row][column] == ' '

    def set_mark(self, coordinates, mark):
        row, column = coordinates
        # self.game_area[row - 1][column - 1] = mark
        self.game_area[row][column] = mark
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


class TicTacToeAIMedium(TicTacToeAI):
    def __init__(self):
        super().__init__()
        self.game_area_dict = {number: ' ' for number in range(9)}
        self.game_level = 'medium'

    def start(self):
        while True:
            command = input('Input command: ').split(' ')
            if len(command) == 1 and command[0] == 'exit':
                break
            elif len(command) != 3 or command[0] != 'start':
                print('Bad parameters!')
                continue
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'medium':
                self.ai_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'user':
                self.ai_medium_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'medium':
                self.user_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'user':
                self.user_vs_user()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'easy':
                self.ai_vs_ai()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'user':
                self.ai_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'easy':
                self.user_vs_ai()
            self.game_area = self.gen_game_area()
            print()

    def ai_vs_ai_medium(self):
        self.render_state()
        while True:
            print(f'Making move level "{self.game_level}"')
            coordinates = self.medium_ai()
            mark = self.x_or_o()
            self.set_mark(coordinates, mark)
            self.render_state()
            state = self.check_state()
            if state:
                print(state)
                return None

    def user_vs_ai_medium(self):
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
                print(f'Making move level "{self.game_level}"')
                coordinates = self.medium_ai()
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

    def ai_medium_vs_user(self):
        self.render_state()
        while True:
            print(f'Making move level "{self.game_level}"')
            coordinates = self.medium_ai()
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

    def medium_ai(self):
        mark = self.x_or_o()
        check_game_area = [''.join(item) for item in self.game_area]
        check_game_area.append(''.join((self.game_area[0][0], self.game_area[1][1], self.game_area[2][2])))
        check_game_area.append(''.join((self.game_area[0][2], self.game_area[1][1], self.game_area[2][0])))
        check_game_area.append(''.join((self.game_area[0][0], self.game_area[1][0], self.game_area[2][0])))
        check_game_area.append(''.join((self.game_area[0][1], self.game_area[1][1], self.game_area[2][1])))
        check_game_area.append(''.join((self.game_area[0][2], self.game_area[1][2], self.game_area[2][2])))
        for idx, row in enumerate(check_game_area):
            if row.count(mark) == 2:
                if 0 <= idx <= 2:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx, idx_2
                if idx == 3:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, idx_2
                if idx == 4:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, abs(idx_2 - 2)
                if idx == 5:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 0
                if idx == 6:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 1
                if idx == 7:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 2
        if mark == 'X':
            mark = 'O'
        else:
            mark = 'X'
        for idx, row in enumerate(check_game_area):
            if row.count(mark) == 2:
                if 0 <= idx <= 2:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx, idx_2
                if idx == 3:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, idx_2
                if idx == 4:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, abs(idx_2 - 2)
                if idx == 5:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 0
                if idx == 6:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 1
                if idx == 7:
                    idx_2 = row.find(' ')
                    if idx_2 != -1:
                        return idx_2, 2
        move_rival_coordinates = super().rival_ai()
        return move_rival_coordinates


def main():
    tictactoe_ai = TicTacToeAIMedium()
    tictactoe_ai.start()


if __name__ == '__main__':
    main()


"""
Stage 4/5: Signs of intelligence

Description

Let's write the medium difficulty level now. To do this, we need to add awareness to our AI.

This level will be a lot harder to beat than easy, even though the initial moves are still random.
When the AI is playing at medium level, it wins when it can because of its first rule, and stops all simple attempts to beat it due to its second.

You can see these rules below.

Objectives

When the AI is playing at medium difficulty level, it makes moves using the following logic:

If it already has two in a row and can win with one further move, it does so.
If its opponent can win with one move, it plays the move necessary to block this.
Otherwise, it makes a random move.
You should add a medium parameter so that you can play against this level.
It should also be possible to make AIs using easy and medium levels play against each other!

Example

The example below shows how your program should work.
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Input command: > start user medium
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
Making move level "medium"
---------
|       |
|   X   |
| O     |
---------
Enter the coordinates: > 1 1
---------
| X     |
|   X   |
| O     |
---------
Making move level "medium"
---------
| X     |
|   X   |
| O   O |
---------
Enter the coordinates: > 3 2
---------
| X     |
|   X   |
| O X O |
---------
Making move level "medium"
---------
| X O   |
|   X   |
| O X O |
---------
Enter the coordinates: > 2 1
---------
| X O   |
| X X   |
| O X O |
---------
Making move level "medium"
---------
| X O   |
| X X O |
| O X O |
---------
Enter the coordinates: > 1 3
---------
| X O X |
| X X O |
| O X O |
---------
Draw

Input command: > start medium user
---------
|       |
|       |
|       |
---------
Making move level "medium"
---------
|       |
|       |
|   X   |
---------
Enter the coordinates: > 2 2
---------
|       |
|   O   |
|   X   |
---------
Making move level "medium"
---------
|       |
|   O   |
| X X   |
---------
Enter the coordinates: > 3 3
---------
|       |
|   O   |
| X X O |
---------
Making move level "medium"
---------
| X     |
|   O   |
| X X O |
---------
Enter the coordinates: > 2 1
---------
| X     |
| O O   |
| X X O |
---------
Making move level "medium"
---------
| X     |
| O O X |
| X X O |
---------
Enter the coordinates: > 1 3
---------
| X   O |
| O O X |
| X X O |
---------
Making move level "medium"
---------
| X X O |
| O O X |
| X X O |
---------
Draw

Input command: > exit
"""