import copy
import time


class Fruits(object):
    board = 0
    board_size = 0
    total_count = 0
    output_file = ""
    number_of_fruits_selected = 0
    prune_count = 0
    count = 0

    def __init__(self, board_size, board, output_file, depth):
        self.output_file = output_file
        self.board = board
        self.board_size = board_size

        board_copy = copy.deepcopy(board)
        possible_moves = self.possible_positions(board_copy)
        max_score, new_board, self.number_of_fruits_selected, bestVal = self.alphabeta(0, 0, True, possible_moves, board,
                                                                              -float("inf"), float("inf"), depth)
        print "max_score", max_score
        print "bestVal", bestVal
        self.printMatrix(new_board)
        print "total_count", self.total_count

    def numberOfFruitsSelected(self):
        return self.number_of_fruits_selected ** 2

    def printMatrix(self, matrix1):

        a = ""
        for i in range(self.board_size):
            b = []
            for j in range(self.board_size):
                b.append(matrix1[i][j])
            a = a + "".join(b) + "\n"

        print a
        output = open(self.output_file, "w")
        output.write(str(self.board_size) + "\n" + a)
        output.close()

    def possible_positions(self, board):

        self.count += 1
        possible_moves = {}
        visited_board = self.addEle()

        for i in range(self.board_size):

            for j in range(self.board_size):

                if visited_board[i][j] == True or board[i][j] == '*':
                    continue

                else:
                    visited_board[i][j] = True
                    move_set = self.playGame(board, visited_board, i, j, board[i][j], set())
                    move_set.add((i, j))
                    move_len = len(move_set)

                    try:
                        possible_moves[move_len].append(move_set)

                    except:
                        possible_moves[move_len] = [move_set]

        # print "PM", possible_moves
        return possible_moves

    def addEle(self):
        return [[False for i in range(self.board_size)] for j in range(self.board_size)]

    def possible_positions1(self, board):

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

    def alphabeta(self, my_score, opponent_score, my_turn, possible_moves, board, alpha, beta, depth):

        # print "in alphabeta"
        # raw_input()
        self.total_count += 1
        if (len(possible_moves) == 0 or depth == 0):
            # print "my_score", my_score
            # print "opp", opponent_score
            return (my_score - opponent_score, None, 0, set())

        else:

            if my_turn:

                # print "Max"
                bestboard = None
                bestfruit = 0
                bestval = set()
                for move, val in sorted(possible_moves.items(), reverse=True):
                    #print "move", move
                    #print "val", val

                    for v in val:

                        board_copy = copy.deepcopy(board)
                        board_copy = self.makeStars(board_copy, v)
                        new_positions = self.possible_positions(board_copy)
                        # print "MY score", my_score, "opponent_score", opponent_score, "positions", new_positions, "board\n", self.printMatrix(board_copy)
                        # raw_input()

                        score, position, move1, val1 = self.alphabeta(my_score + (move ** 2), opponent_score, not my_turn,
                                                                new_positions, board_copy, alpha, beta,
                                                                depth - 1)
                        if score > alpha:
                            alpha = score
                            bestboard = board_copy
                            bestval = v

                        if alpha >= beta:
                            self.prune_count += 1
                            return (alpha, bestboard, bestfruit, bestval)

                return (alpha, bestboard, bestfruit, bestval)

            else:

                bestboard = None
                bestfruit = 0
                bestval = set()
                for move, val in sorted(possible_moves.items(), reverse=True):
                    for v in val:
                        board_copy = copy.deepcopy(board)
                        board_copy = self.makeStars(board_copy, v)
                        new_positions = self.possible_positions(board_copy)
                        # print "MY score", my_score, "opponent_score", opponent_score, "positions", new_positions, "board\n", self.printMatrix(board_copy)
                        # raw_input()

                        score, position, move1, val1 = self.alphabeta(my_score, opponent_score + (move ** 2), not my_turn,
                                                                new_positions, board_copy, alpha, beta,
                                                                depth - 1)
                        if score < beta:
                            beta = score
                            bestboard = board_copy
                            bestfruit = move
                            bestval = v

                        if alpha >= beta:
                            self.prune_count += 1
                            return (beta, bestboard, bestfruit, bestval)

                return (beta, bestboard, bestfruit, bestval)

    def playGame3(self, board, current_row, current_col, current_fruit, fruit_set):

        row_arr = [-1, 0, 1, 0]
        col_arr = [0, 1, 0, -1]
        board[current_row][current_col] = '+'

        for i in range(4):
            row_inc = current_row + row_arr[i]
            col_inc = current_col + col_arr[i]

            if row_inc != self.board_size and row_inc != -1 and col_inc != self.board_size and col_inc != -1 \
                    and board[row_inc][col_inc] == current_fruit:
                board[row_inc][col_inc] = '+'
                fruit_set.add((row_inc, col_inc))
                self.playGame(board, row_inc, col_inc, current_fruit, fruit_set)

        return fruit_set

    def playGame2(self, board, current_row, current_col, current_fruit, fruit_set):

        while current_row >= 0 and current_row < self.board_size and current_col >= 0 and current_col < self.board_size and \
                        board[current_row][current_col] == current_fruit:
            board[current_row][current_col] = '+'
            fruit_set.add((current_row, current_col))
            self.playGame(board, current_row - 1, current_col, current_fruit, fruit_set)
            self.playGame(board, current_row, current_col - 1, current_fruit, fruit_set)
            self.playGame(board, current_row, current_col + 1, current_fruit, fruit_set)
            self.playGame(board, current_row + 1, current_col, current_fruit, fruit_set)

        return fruit_set

    def playGame4(self, original_board, visited_board, current_row, current_col, current_fruit, fruit_set):

        row_arr = [-1, 0, 1, 0]
        col_arr = [0, 1, 0, -1]
        # print "row, col", current_row, current_col

        for i in range(4):
            row_inc = current_row + row_arr[i]
            col_inc = current_col + col_arr[i]

            if row_inc != self.board_size and row_inc != -1 and col_inc != self.board_size and col_inc != -1 \
                    and original_board[row_inc][col_inc] == current_fruit and visited_board[row_inc][col_inc] == False:
                visited_board[row_inc][col_inc] = True
                fruit_set.add((row_inc, col_inc))
                self.playGame(original_board, visited_board, row_inc, col_inc, current_fruit, fruit_set)

        return fruit_set

    def playGame(self, original_board, visited_board, current_row, current_col, current_fruit, fruit_set):

        queue = [(current_row, current_col)]

        while queue:
            number = queue.pop()
            row, col = number[0], number[1]
            #left Side
            if col-1 > -1 and visited_board[row][col-1] == False and original_board[row][col-1] == current_fruit:
                visited_board[row][col - 1] = True
                fruit_set.add((row, col-1))
                queue.append((row,col-1))
            #right side
            if col+1 < self.board_size and visited_board[row][col+1] == False and original_board[row][col+1] == current_fruit:
                visited_board[row][col + 1] = True
                fruit_set.add((row, col+1))
                queue.append((row, col+1))
            #upper
            if row - 1 > -1 and visited_board[row-1][col] == False and original_board[row-1][col] == current_fruit:
                visited_board[row-1][col] = True
                fruit_set.add((row-1, col))
                queue.append((row-1,col))
            #down
            if row + 1 < self.board_size and visited_board[row+1][col] == False and original_board[row+1][col] == current_fruit:
                visited_board[row+1][col] = True
                fruit_set.add((row+1, col))
                queue.append((row+1, col))

        return fruit_set

    def makeStars(self, board, fruit_coordinates):

        col_dic = {}
        for ele in fruit_coordinates:
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
no_type_of_fruit = int(input_file.readline())
time_remaining = float(input_file.readline())

matrix = []

for i in range(matrix_size):
    row_string = input_file.readline()
    row_int = list(row_string)[:-1]
    matrix.append(row_int)

start_time = time.time()
game = Fruits(matrix_size, matrix, "output.txt", 3)
print (time.time() - start_time) * 1000
print "pc", game.prune_count
print game.numberOfFruitsSelected()
