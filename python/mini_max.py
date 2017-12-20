import copy

class Fruits(object):

    board = 0
    board_size = 0
    total_count = 0
    def __init__(self, board_size, board):
        self.board = board
        self.board_size = board_size
        max_score, new_board = self.miniMaxi(0, 0, True, {}, board, True)
        print "max_score", max_score
        self.printMatrix(new_board)
        print "total_count", self.total_count

    def printMatrix(self, matrix1):

        for i in range(self.board_size):
            b = []
            for j in range(self.board_size):
                b.append(matrix1[i][j])
            print "".join(b)

    def possible_positions(self, board):

        possible_moves = {}
        board_copy = copy.deepcopy(board)

        for i in range(self.board_size):

            for j in range(self.board_size):

                fruit = board_copy[i][j]

                if fruit == '+' or fruit == '*':
                    continue

                move_set = self.playGame(board_copy, i, j, board_copy[i][j], set())
                move_set.add((i, j))

                move_len = len(move_set)

                if move_len in possible_moves:
                    possible_moves[move_len].append(move_set)
                else:
                    possible_moves[move_len] = [move_set]

        return possible_moves

    def miniMaxi(self, my_score, opponent_score, my_turn, possible_moves, board, start):

        #print "in MiniMaxi"
        #raw_input()
        self.total_count += 1

        if len(possible_moves) == 0 and not start:
            return (my_score - opponent_score, None)

        else:

            if start:

                board_copy = copy.deepcopy(board)
                self.printMatrix(board_copy)
                possible_moves = self.possible_positions(board_copy)

            if my_turn:

                #print "Max"
                bestscore = - float("inf")
                bestboard = None

                for move in possible_moves:

                    board_copy = copy.deepcopy(board)
                    board_copy = self.makeStars(move, board_copy, possible_moves)
                    new_positions = self.possible_positions(board_copy)
                    #print "MY score", my_score, "opponent_score", opponent_score, "positions", new_positions, "board\n", self.printMatrix(board_copy)
                    #raw_input()

                    score, position = self.miniMaxi(my_score+move, opponent_score, not my_turn, new_positions, board_copy, False)

                    if score > bestscore:
                        bestscore = score
                        bestboard = board_copy

                return (bestscore, bestboard)

            else:

                bestscore = float("inf")
                bestboard = None
                #print "in Mini"
                for move in possible_moves:

                    board_copy = copy.deepcopy(board)
                    board_copy = self.makeStars(move, board_copy, possible_moves)
                    new_positions = self.possible_positions(board_copy)
                    #print "MY score", my_score, "opponent_score", opponent_score, "positions", new_positions, "board\n", self.printMatrix(board_copy)
                    #raw_input()

                    score, position = self.miniMaxi(my_score, opponent_score + move, not my_turn, new_positions, board_copy, False)
                    if score < bestscore:
                        bestscore = score
                        bestboard = board_copy

                return (bestscore, bestboard)

    def playGame(self, board, current_row, current_col, current_fruit, fruit_set):

        row_arr = [-1, 0, 1, 0]
        col_arr = [0, 1, 0, -1]
        board[current_row][current_col] = '+'

        for i in range(4):
            row_inc = current_row + row_arr[i]
            col_inc = current_col + col_arr[i]

            if row_inc != self.board_size and row_inc != -1 and col_inc != self.board_size and col_inc != -1 \
                    and board[row_inc][col_inc] == current_fruit and board[row_inc][col_inc] != '+' and board[row_inc][col_inc] != '*':

                board[row_inc][col_inc] = '+'
                fruit_set.add((row_inc, col_inc))
                self.playGame(board, row_inc, col_inc, current_fruit, fruit_set)

        return fruit_set

    def makeStars(self, fruit_len, board, fruit_dic):

        col_dic = {}
        for ele in fruit_dic[fruit_len][0]:
            (row, col) = ele
            board[row][col] = '+'

            if not col in col_dic:
                col_dic[col] = row
            elif col_dic[col] < row:
                col_dic[col] = row

        for col in col_dic:
            self.updateCol(col_dic[col], col, board),

        return board

    def updateCol(self, row, col, board):

        j = row
        while j > -1:
            if board[j][col] != '+':
                board[row][col] = board[j][col]
                board[j][col] = '*'
                row = row - 1
            else:
                board[row][col] = '*'
            j = j - 1

        for i in range(row, -1, -1):
            board[i][col] = '*'

        return board

input_file = open("input.txt")
matrix_size = int(input_file.readline())
matrix = []
for i in range(matrix_size):
    row_string = input_file.readline()
    row_int = list(row_string)[:-1]
    matrix.append(row_int)

game = Fruits(matrix_size, matrix)
