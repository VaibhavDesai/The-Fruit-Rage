import sys

def gravity(size,bin):
	#when fruits encounter gravity
	for col in range(size):
		star=size-1
		for row in range(size-1,-1,-1):
			if bin[row][col]!='*':
				bin[row][col],bin[star][col]=bin[star][col],bin[row][col]
				star-=1

def moveCheck(size,pos,bin,bout):
	#check if the move is valid:
	#whether the move is inside the board
	#whether the move is on a fruit
	#whether the result is right after move and gravity
	col,row=ord(pos[0])-ord('A'),int(pos[1:])-1
	if col>=size or row>=size:
		return False

	#sink the same type fruit
	mark=bin[row][col]
	if mark=='*':
		return False
	def sink(i,j):
		if 0<=i<size and 0<=j<size and bin[i][j]==mark:
			bin[i][j]='*'
			list(map(sink,(i-1,i+1,i,i),(j,j,j-1,j+1)))
	sink(row,col)
	#print(bin)
	
	gravity(size,bin)
	#print(bin)

	#return not len([(i,j) for i in range(size) for j in range(size) if bin[i][j]!=bout[i][j]])
	return bin==bout

def readoutput(filename,size):
	#read output.txt
	#check the format of output.txt
	#return pos of move and board, if wrong ans then return '',[]
	try:
		with open(filename,'r') as file:
			#FAIL if ' G8' and 'g8' and '58' and 'G8i'
			pos=file.readline()
			if not len(pos) or not pos[0].isupper():
				return '',[]
			pos=pos.strip()
			if not pos[1:].isdigit():
				return '',[]

			#FAIL if empty space before first char and not right length
			board=[]
			for _ in range(size):
				l=file.readline()
				if not len(l) or (l[0]!='*' and not l[0].isdigit()):
					return '',[]
				l=l.strip()
				if len(l)!=size:
					return '',[]
				board.append(list(l))
	except Exception:
		return '',[]

	return pos,board

def readinput(filename):
	#read input.txt
	#return size of board and board
	with open(filename,'r') as file:
		size=int(file.readline().strip())
		fruit=int(file.readline().strip())
		time=float(file.readline().strip())
		board=[list(file.readline().strip()) for _ in range(size)]

	return size,board

def ansCheck(intxt,outxt):
	#read and check
	size,bin=readinput(intxt)
	pos,bout=readoutput(outxt,size)

	return pos and moveCheck(size,pos,bin,bout)

if __name__ == "__main__":
	# print(sys.argv[1])
	# print(sys.argv[2])

	if ansCheck(sys.argv[1],sys.argv[2]):
		print('PASS')
	else:
		print('FAIL')