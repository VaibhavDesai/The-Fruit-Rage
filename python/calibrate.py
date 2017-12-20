from alpha_beta import Fruits
import time

def generate_board():

    b = ['0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5']
    c = ['9','8','7','6','5','4','3','2','1','0','9','8','7','6','5','4','3','2','1','0','9','8','7','6','5','4']

    matrix = []
    for i in range(26):
        if i%2 == 0:
            matrix.append(b)
        else:
            matrix.append(c)

    return matrix

def generate_submatrix(matrix_size, original_matrix):

    sub_matrix = []
    for i in range(matrix_size):
        sub_matrix_col = []
        for j in range(matrix_size):
            sub_matrix_col.append(original_matrix[i][j])
        sub_matrix.append(sub_matrix_col)

    #print sub_matrix
    return sub_matrix

def run_algo():

    original_matrix = generate_board()

    start_time1 = time.time()
    output = open("calibrate.txt", "a")
    a = ""
    for i in range(6):
        submatrix_size = i
        for j in range(3,9):
            submatrix_depth = j
            print submatrix_depth
            submatrix = generate_submatrix(submatrix_size, original_matrix)
            start_time = time.time()
            game = Fruits(submatrix_size, submatrix, "output.txt", submatrix_depth)
            time_taken = (time.time() - start_time)
            print time_taken
            a += str(time_taken)+" "
        a += "\n"

    output.write(a)
    print (time.time() - start_time1)



run_algo()