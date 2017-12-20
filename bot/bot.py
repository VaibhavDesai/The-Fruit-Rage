from alpha_beta import Fruits

def readInputFile(file_name):

    input_file = open(file_name)
    matrix_size = int(input_file.readline())
    input_matrix = []
    for i in range(matrix_size):
        row_string = input_file.readline()
        row_int = list(row_string)[:-1]
        input_matrix.append(row_int)

    return matrix_size, input_matrix

def checkIfGameIsOver(input_matrix):

    isOver = True
    for row in input_matrix:
        for j in row:
            if j != '*':
                isOver = False
                break
    return isOver

def resetBoard(copy_from_file, copy_to_file):
    with open(copy_to_file, 'w+') as output, open(copy_from_file, 'r') as input:
        while True:
            data = input.read(100000)
            if data == '':  # end of file reached
                break
            output.write(data)

resetBoard("input1.txt", "botinput.txt")
matrix_size, input_matrix = readInputFile("botinput.txt")
player1 = True
player1_points = 0
player2_points = 0
no_of_turns = 0

while not checkIfGameIsOver(input_matrix):
    no_of_turns +=1
    if player1:
        print "player1"
        player1_points += Fruits(matrix_size, input_matrix, "botinput.txt", 2).numberOfFruitsSelected()
        print player1_points
    else:
        print "player2"
        player2_points += Fruits(matrix_size, input_matrix, "botinput.txt", 1).numberOfFruitsSelected()
        print player2_points

    player1 = not player1
    matrix_size, input_matrix = readInputFile("botinput.txt")

print "points \n player1:", player1_points, "player2:", player2_points
print "no_of_turns",no_of_turns/2
