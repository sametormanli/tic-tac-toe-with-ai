import random
import copy


class TicTacToe:
    def __init__(self, cells=None, turn=True):
        self.turn = turn
        self.cells = self.matrix_from_str(cells)

    def matrix_from_str(self, string):
        if string is None:
            return [[' ' for _ in range(3)] for __ in range(3)]
        counter = 0
        for char in string:
            if char == 'X':
                counter += 1
            if char == 'O':
                counter -= 1
        if counter > 0:
            self.turn = False
        return [[item if item in ('X', 'O') else ' ' for item in string[i:i + 3]] for i in range(0, 7, 3)]

    def converter(self, lst, flat):
        if flat:
            return [item for row in lst for item in row]
        return [[item for item in lst[i:i + 3]] for i in range(0, 7, 3)]

    def state(self, cells):
        for row in cells:
            if row[0] == row[1] == row[2] and row[0] != ' ':
                return row[0]
        for i in range(3):
            if cells[0][i] == cells[1][i] == cells[2][i] and cells[0][i] != ' ':
                return cells[0][i]
        if (cells[0][0] == cells[1][1] == cells[2][2] or cells[1][1] == cells[0][2] == cells[2][0]) and cells[1][
            1] != ' ':
            return cells[1][1]
        if ' ' not in self.converter(cells, True):
            return 'draw'
        return 'continue'

    def mark(self, row, col):
        self.cells[row][col] = 'X' if self.turn else 'O'
        self.turn = not self.turn

    def print_board(self):
        print('''---------
               \r| {} {} {} |
               \r| {} {} {} |
               \r| {} {} {} |
               \r---------'''.format(*self.converter(self.cells, True)))

    def entry(self):
        while True:
            try:
                row, col = [int(num) for num in input('Enter the coordinates: ').split()]
            except (IndexError, ValueError):
                print('You should enter numbers!')
                continue
            if row not in range(1, 4) or col not in range(1, 4):
                print('Coordinates should be from 1 to 3!')
                continue
            row, col = 3 - col, row - 1
            if self.cells[row][col] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            return row, col

    def easy(self):
        possibles = [i for i in range(9) if self.converter(self.cells, True)[i] == ' ']
        choice = random.choice(possibles)
        return divmod(choice, 3)

    def medium(self):
        look = 'X' if self.turn else 'O'
        first_check = self.last_move(self.cells, look)
        if first_check is not None:
            return first_check
        anti_look = 'O' if self.turn else 'X'
        second_check = self.last_move(self.cells, anti_look)
        if second_check is not None:
            return second_check
        return self.easy()

    def last_move(self, cells, look):
        for i in range(3):
            for j in range(3):
                if cells[i][j] == ' ':
                    check_1 = cells[i][(j + 1) % 3] == cells[i][(j + 2) % 3] == look
                    check_2 = cells[(i + 1) % 3][j] == cells[(i + 2) % 3][j] == look
                    check_3 = None
                    if i == j == 0 or i == j == 1 or i == j == 2:
                        check_3 = cells[(i + 1) % 3][(j + 1) % 3] == cells[(i + 2) % 3][(j + 2) % 3] == look
                    if (i == 0 and j == 2) or (i == j == 1) or (i == 2 and j == 0):
                        check_3 = cells[(i + 1) % 3][(j - 1) % 3] == cells[(i + 2) % 3][(j - 2) % 3] == look
                    if any([check_1, check_2, check_3]):
                        return i, j

    def minmax(self, cells, sign, depth):
        current_state = self.state(cells)
        if current_state == 'draw':
            return 0
        elif current_state in ('X', 'O'):
            return -1 if depth % 2 else 1
        else:
            subs = []
            for i in range(3):
                for j in range(3):
                    if cells[i][j] == ' ':
                        clone = copy.deepcopy(cells)
                        clone[i][j] = 'O' if sign else 'X'
                        subs.append(self.minmax(clone, not sign, depth + 1))
            return max(subs) if depth % 2 else min(subs)

    def hard(self):
        possible = []
        clone = copy.deepcopy(self.cells)
        for i in range(3):
            for j in range(3):
                if clone[i][j] == ' ':
                    clone[i][j] = 'X' if self.turn else 'O'
                    minimax = self.minmax(clone, self.turn, 0)
                    possible.append([minimax, i, j])
                    clone[i][j] = ' '
        maximum = max(item[0] for item in possible)
        for item in possible:
            if item[0] == maximum:
                return item[1], item[2]

    def main(self):
        words = ('user', 'easy', 'medium', 'hard')
        while True:
            try:
                entry = input('Input command: ')
                if entry == 'exit':
                    print('Bye!')
                    exit()
                word1, word2, word3 = entry.split()
                if word1 != 'start' or word2 not in words or word3 not in words:
                    raise ValueError
            except ValueError:
                print('Bad parameters!')
                continue
            break
        self.play(word2, word3)

    def player(self, string):
        if string == 'user':
            return self.entry()
        if string == 'easy':
            return self.easy()
        if string == 'medium':
            return self.medium()
        if string == 'hard':
            return self.hard()

    def play(self, player_1, player_2):
        self.print_board()
        while self.state(self.cells) == 'continue':
            player = player_1 if self.turn else player_2
            if player != 'user':
                print(f'Making move level "{player}"')
            self.mark(*self.player(player))
            self.print_board()
            if self.state(self.cells) == 'continue':
                print('Game not finished\n')
        result = self.state(self.cells)
        print('\nDraw' if result == 'draw' else '\n*-_-*-_-*   ' + result + ' wins   *-_-*-_-*')


game = TicTacToe()
game.main()