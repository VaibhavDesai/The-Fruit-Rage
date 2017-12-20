import copy
import time

def gravity(size,bin):
	#when fruits encounter gravity
	for col in range(size):
		star=size-1
		for row in range(size-1,-1,-1):
			if bin[row][col]!='*':
				bin[row][col],bin[star][col]=bin[star][col],bin[row][col]
				star-=1

def result(size,board,move):
	#only sink fruit to save n^2 time
	fruit=[]
	x,y=move
	mark=board[x][y]
	def sink(i,j):
		if 0<=i<size and 0<=j<size and board[i][j]==mark:
			board[i][j]='*'
			fruit.append('f')
			list(map(sink,(i-1,i+1,i,i),(j,j,j-1,j+1)))
	sink(x,y)
	# gravity(size,board)
	return board,len(fruit)**2

def cutoff(size,board):
	#same as terminal test
	return not len([(i,j) for i in range(size) for j in range(size) if board[i][j]!='*'])

def maxValue(size,board,cumulate_reward,depth_limit):
	if not depth_limit or cutoff(size,board):
		return cumulate_reward
	max_val=-2**31
	explored=set()
	moves=[(i,j) for i in range(size) for j in range(size) if board[i][j]!='*']
	for m in moves:
		tmpboard,reward=result(size,copy.deepcopy(board),m)
		if str(tmpboard) in explored:
			continue
		else:
			explored.add(str(tmpboard))
		gravity(size,tmpboard)
		min_eval=minValue(size,tmpboard,cumulate_reward+reward,depth_limit-1)
		max_val=max(min_eval,max_val)

	return max_val

def minValue(size,board,cumulate_reward,depth_limit):
	if not depth_limit or cutoff(size,board):
		return cumulate_reward
	min_val=2**31-1
	explored=set()
	moves=[(i,j) for i in range(size) for j in range(size) if board[i][j]!='*']
	for m in moves:
		tmpboard,reward=result(size,copy.deepcopy(board),m)
		if str(tmpboard) in explored:
			continue
		else:
			explored.add(str(tmpboard))
		gravity(size,tmpboard)
		max_eval=maxValue(size,tmpboard,cumulate_reward-reward,depth_limit-1)
		min_val=min(max_eval,min_val)
	
	return min_val

def minimax(size,board,depth_limit=1):
	max_val=-2**31
	explored=set()
	moves=[(i,j) for i in range(size) for j in range(size) if board[i][j]!='*']
	for m in moves:
		tmpboard,reward=result(size,copy.deepcopy(board),m)
		if str(tmpboard) in explored:
			continue
		else:
			explored.add(str(tmpboard))
		gravity(size,tmpboard)
		min_eval=minValue(size,tmpboard,reward,depth_limit-1)
		if min_eval>max_val:
			max_val=min_eval
			bestmove=m

	return bestmove

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
		remain=float(file.readline().strip())
		board=[list(file.readline().strip()) for _ in range(size)]

	return size,fruit,remain,board

if __name__ == "__main__":
	#tick-tick
	# start=time.clock()

	#read file
	size,fruit,remain,board=readinput('input.txt')

	#minimax select one move
	x,y=minimax(size,copy.deepcopy(board))

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

	# end=time.clock()
	# print('Runtime: {0} s'.format(end-start))