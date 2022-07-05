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
                coordinates = [int(x) - 1 for x in input('Enter the coordinates: ') if x != ' ']
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


class TicTacToeAImedium(TicTacToeAI):
    def __init__(self):
        super().__init__()
        self.game_level = 'medium'

    def start(self):
        while True:
            command = input('Input command: ').split(' ')
            if len(command) == 1 and command[0] == 'exit':
                break
            elif len(command) != 3 or command[0] != 'start':
                print('Bad parameters!')
                continue
            elif command[0] == 'start' and command[1] == 'hard' and command[2] == 'hard':
                self.game_level = 'hard'
                self.ai_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'hard' and command[2] == 'user':
                self.ai_medium_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'hard':
                self.game_level = 'hard'
                self.user_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'medium':
                self.game_level = 'medium'
                self.ai_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'user':
                self.game_level = 'medium'
                self.ai_medium_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'medium':
                self.game_level = 'medium'
                self.user_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'user':
                self.user_vs_user()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'easy':
                self.game_level = 'easy'
                self.ai_vs_ai()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'user':
                self.game_level = 'easy'
                self.ai_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'easy':
                self.game_level = 'easy'
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


class TicTacToeAIhard(TicTacToeAImedium, TicTacToeAI):
    def __init__(self):
        super().__init__()

    def start(self):
        while True:
            command = input('Input command: ').split(' ')
            if len(command) == 1 and command[0] == 'exit':
                break
            elif len(command) != 3 or command[0] != 'start':
                print('Bad parameters!')
                continue
            elif command[0] == 'start' and command[1] == 'hard' and command[2] == 'hard':
                self.game_level = 'hard'
                self.ai_vs_ai_hard()
            elif command[0] == 'start' and command[1] == 'hard' and command[2] == 'user':
                self.ai_hard_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'hard':
                self.game_level = 'hard'
                self.user_vs_ai_hard()
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'medium':
                self.game_level = 'medium'
                self.ai_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'medium' and command[2] == 'user':
                self.game_level = 'medium'
                self.ai_medium_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'medium':
                self.game_level = 'medium'
                self.user_vs_ai_medium()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'user':
                self.user_vs_user()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'easy':
                self.game_level = 'easy'
                self.ai_vs_ai()
            elif command[0] == 'start' and command[1] == 'easy' and command[2] == 'user':
                self.game_level = 'easy'
                self.ai_vs_user()
            elif command[0] == 'start' and command[1] == 'user' and command[2] == 'easy':
                self.game_level = 'easy'
                self.user_vs_ai()
            self.game_area = self.gen_game_area()
            print()

    def ai_vs_ai_hard(self):
        self.render_state()
        while True:
            print(f'Making move level "{self.game_level}"')
            coordinates = self.hard_ai()
            mark = self.x_or_o()
            self.set_mark(coordinates, mark)
            self.render_state()
            state = self.check_state()
            if state:
                print(state)
                return None

    def user_vs_ai_hard(self):
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
                coordinates = self.hard_ai()
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

    def ai_hard_vs_user(self):
        self.render_state()
        while True:
            print(f'Making move level "{self.game_level}"')
            coordinates = self.hard_ai()
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

    def hard_ai(self):
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
        if self.is_empty((1, 1)):
            return 1, 1
        move_rival_coordinates = super().rival_ai()
        return move_rival_coordinates


def main():
    tictactoe_ai = TicTacToeAIhard()
    tictactoe_ai.start()


if __name__ == '__main__':
    main()


"""
Stage 5/5: An undefeated champion

Description

Congratulations, you've almost reached the finish line! To complete the task, it's now time to turn the AI into a strong opponent by adding a hard difficulty level.

Unlike medium, when the AI is playing at hard level, it doesn't just look one move ahead to see an immediate win or prevent an immediate loss.
At this level, it can look two moves ahead, three moves ahead, and even further.
It can calculate all possible moves that might be played during the game, and choose the best one based on the assumption that its opponent will also play perfectly.
So, it doesn't rely on the mistakes of its opponent and plays the game without fault from start to finish regardless of the opponent's skill!

The algorithm that implements this is called minimax. It's a brute force algorithm that maximizes the value of the AI's position and minimizes the worth of its opponent's.
Minimax is not just for Tic-Tac-Toe. You can use it with any other game where two players make alternate moves, such as chess.

Objectives

In this last stage, you need to implement the hard difficulty level using the minimax algorithm.

You should also add a hard parameter so that it's possible to play against this level.

Example

The example below shows how your program should work.
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Input command: > start hard user
Making move level "hard"
---------
|       |
| X     |
|       |
---------
Enter the coordinates: > 2 2
---------
|       |
| X O   |
|       |
---------
Making move level "hard"
---------
|   X   |
| X O   |
|       |
---------
Enter the coordinates: > 3 2
---------
|   X   |
| X O   |
|   O   |
---------
Making move level "hard"
---------
| X X   |
| X O   |
|   O   |
---------
Enter the coordinates: > 3 1
---------
| X X   |
| X O   |
| O O   |
---------
Making move level "hard"
---------
| X X X |
| X O   |
| O O   |
---------
X wins

Input command: > exit
"""