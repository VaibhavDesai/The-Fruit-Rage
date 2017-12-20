import random

def gravity(size,bin):
	#when fruits encounter gravity
	for col in range(size):
		star=size-1
		for row in range(size-1,-1,-1):
			if bin[row][col]!='*':
				bin[row][col],bin[star][col]=bin[star][col],bin[row][col]
				star-=1
				
def writeoutput(filename,pos,board):
	#write output.txt
	#boring function and boring output
	with open(filename,'w') as file:
		file.write(pos+'\n')
		[file.write(''.join(l)+'\n') for l in board]

def readinput(filename):
	#read input.txt
	#return size of board, fruit type and board
	with open(filename,'r') as file:
		size=int(file.readline().strip())
		fruit=int(file.readline().strip())
		time=float(file.readline().strip())
		board=[list(file.readline().strip()) for _ in range(size)]

	return size,fruit,board

if __name__ == "__main__":
	#read file
	size,fruit,board=readinput('input.txt')
	
	#random select one valid move
	validms=[(i,j) for i in range(size) for j in range(size) if board[i][j]!='*']
	x,y=random.choice(validms)
	
	#move and gravity
	mark=board[x][y]
	def sink(i,j):
		if 0<=i<size and 0<=j<size and board[i][j]==mark:
			board[i][j]='*'
			list(map(sink,(i-1,i+1,i,i),(j,j,j-1,j+1)))
	sink(x,y)
	gravity(size,board)
	
	#print result
	pos='{}{}'.format(chr(y+ord('A')),x+1)
	writeoutput('output.txt',pos,board)
	# print(pos)
	# [print(''.join(l)) for l in board]