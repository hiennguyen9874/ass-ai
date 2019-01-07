
import imp
import time
#======================================================================


def board_print(board, move=[], num=0):

    print("====== The current board(", num, ") is (after move): ======")
    if move: # move not empty
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")


def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board

#======================================================================

# Student SHOULD implement this function to change current state to new state properly

# Create dictionary for future use
neighborDict = {}
adjacentDict = {}
neighborPosL = []
adjacentPosL = []
for r in range(5):
    for c in range(5):
        neighborPosL = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c), (r - 1, c - 1), (r + 1, c + 1), (r - 1, c + 1), (r + 1, c - 1)]
        if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
            adjacentPosL = [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            adjacentPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), adjacentPosL) )
            neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            neighborDict[r*5 + c] = neighborPosL
            adjacentDict[r*5 + c] = adjacentPosL
        else:
            adjacentPosL = neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            adjacentDict[r*5 + c] = neighborDict[r*5 + c] = neighborPosL
        
        adjacentPosL = neighborPosL = []


def traverse_CHET(startPos, currColor, oppColor, state, q = []):
    # startPos: starting position for traversing; (r, c)
    # currColor: current player's color
    # oppColor: opponent's color
    # state: board game
    # q: list saving opponents' positions of which colors were changed
    # return True if no way out, else False
    
    # index = startPos[0]*5 + startPos[1]
    # aL = adjacentDict[index]
    #state[ startPos[0] ][ startPos[1] ] = currColor
    
    ############################### DFS
    
    state[ startPos[0] ][ startPos[1] ] = currColor
    q.append(startPos)
    for x in adjacentDict[ startPos[0]*5 + startPos[1] ]:
        if (state[ x[0] ][ x[1] ] == '.') or ( state[ x[0] ][ x[1] ] == oppColor and ( not traverse_CHET(x, currColor, oppColor, state, q) ) ):
            while(q[-1] != startPos):
                state[ q[-1][0] ][ q[-1][1] ] = oppColor
                q.pop()
            state[ startPos[0] ][ startPos[1] ] = oppColor
            q.pop()
            return False
            
    return True
    
    ############################### BFS
    #l = []
    # state[ startPos[0] ][ startPos[1] ] = currColor
    # q.append(startPos)
    
    # for x in l:
        # if state[ x[0] ][ x[1] ] == oppColor and ( not traverse_CHET(x, currColor, oppColor, state, q) ):
            # while(q[-1] != startPos)
                # state[ q[-1][0] ][ q[-1][1] ] = oppColor
                # q.pop()
            # state[ startPos[0] ][ startPos[1] ] = oppColor
            # q.pop()
            # return False
            
            # #l.append(x)
            
    # return True

def doit(move, state, a):
    # move: a list of two tuples 
        # (row0, col0): current position of selected piece
        # (row1, col1): new position of selected piece
    # state: a list of 5 list, simulating the game board
    # a: a list of anything (if needed) [curr_player, board_num, state, move, [list of traps (if exist)]]
    
    if not move or not state:
        return None
    #else:
    if move[0] == move[1]:
        return None
    
    row0 = move[0][0]
    col0 = move[0][1]
    row1 = move[1][0]
    col1 = move[1][1]
    
    if row0 not in range(5) or col0 not in range(5) or row1 not in range(5) or col1 not in range(5):
        return None
    if state[ row0 ][ col0 ] == '.' or state[ row1 ][ col1 ] in ['b', 'r']:
        return None
    if state[row0][col0] != str(a[0]):
        return None
    #else: # check if two points are adjacent
    index0 = row0*5 + col0
    index1 = row1*5 + col1
    if move[1] not in adjacentDict[index0]:
        return None
    
    # if (row1 - row0) not in [-1, 0, 1] or (col1 - col0) not in [-1, 0, 1]:
        # return None
    # # evenL = [0, 2, 4]
    # # oddL = [1, 3]
    # isDiagonal = True
    # if (row0 % 2 == 0 and col0 % 2 != 0) or (row0 % 2 != 0 and col0 % 2 == 0):
        # isDiagonal = False
        # if (row1 - row0) in [-1, 1] and (col1 - col0) in [-1, 1]: # not allow to move diagonally in these positions
            # return None
    
    #else: # the move is valid except when previous move is a trapping move, we should do more check @@
    if a[1] == 0: # starting point of the game, the first move
        #a.append(state) # previous board game
        #a.append(move) # current move now considered as previous move
        a.append([]) # list of tuples containing positions of traps created by previous move
        
        #TODO: make some changes to the state
        # create new board for the legal move
        new_state = board_copy(state)
        new_state[row0][col0] = '.'
        new_state[row1][col1] = state[row0][col0]
        
        return new_state
        
    #else: # should check the previous move and compare the previous state with the current state
    #isTrapping = False
    if a[-1]: # trapped turn
        #isTrapping = True
        #print(a[-1])
        if move[1] not in a[-1]: # previous move is a trapping move, so check for the current move correctness
            return None
        a[-1] = [] # no need of saving these traps anymore
        
    #TODO: make some changes to the state
    
    
    # if isDiagonal:
        # pL = [(row1 - 1, col1 - 1), (row1 - 1, col1), (row1 - 1, col1 + 1), (row1, col1 - 1), (row1, col1 + 1), (row1 + 1, col1 - 1), (row1 + 1, col1), (row1 + 1, col1 + 1)]
    # else:
        # pL = [(row1 - 1, col1), (row1, col1 - 1), (row1, col1 + 1), (row1 + 1, col1)]
    
    currColor = state[row0][col0]
    oppColor = 'r' if currColor == 'b' else 'b'
    
    # oppL = list(filter(lambda x: x[0] in range(5) and x[1] in range(5) and x != move[0] and state[ x[0] ][ x[1] ] not in ['.', currColor], pL)) # list saving positions around the target point which have the opponent's chessmans
    
    #new_state = board_copy(state)
    new_state = state
    new_state[row1][col1] = currColor
    new_state[row0][col0] = '.'
    
    sameL = []
    oppL = []
    pointL = []
    for x in adjacentDict[index1]:
        if new_state[ x[0] ][ x[1] ] == oppColor:
            oppL.append(x)
        elif new_state[ x[0] ][ x[1] ] == currColor:
            sameL.append(x)
        elif x != move[0]:
            pointL.append(x)
    
    #oppL = list(filter(lambda x: state[ x[0] ][ x[1] ] == oppColor, adjacentDict[index1])) # list saving positions around the target point which have the opponent's chessmans
    
    isChanged = False
    
    ################################# "Ganh":
    
    # for x in adjacentDict[index1]:
        # if state[ x[0] ][ x[1] ] not in ['.', currColor]:
            # yR = row1*2 - x[0]
            # yC = col1*2 - x[1]
            # if yR in range(5) and yC in range(5) and state[ yR ][ yC ] not in ['.', currColor]: # then "ganh"
                # new_state[ x[0] ][ x[1] ] = currColor
                # new_state[ yR ][ yC ] = currColor
                # isChanged = True
    
    changedL = [] # list saving chessman positions of which colors are changed
    newOppL = []
    for x in oppL:
        if new_state[ x[0] ][ x[1] ] == oppColor:
            yR = row1*2 - x[0] # find the
            yC = col1*2 - x[1] # symmetric point
            if ( 0 <= yR < 5 ) and ( 0 <= yC < 5 ) and (new_state[ yR ][ yC ] == oppColor): # then "ganh"
                new_state[ x[0] ][ x[1] ] = currColor
                new_state[ yR ][ yC ] = currColor
                isChanged = True
                changedL.append(x)
                changedL.append( (yR, yC) )
            else:
                newOppL.append(x)
    
    # pL = oppL[:]
    # i = 0
    # j = 1
    # isFound = False
    # while len(pL) > 1:
        # while j < len(pL)
            # if ( (pL[j][0] + pl[i][0])/2, (pL[j][1] + pL[i][1])/2 ) == move[1]: # if symmetry
                # new_state[pL[j][0][pL[j][1]] = currColor
                # new_state[pL[i][0]][pL[i][1]] = currColor
                # pL.pop(i)
                # pL.pop(j - 1)
                # isFound = True
                # isChanged = True
                # break
            # j += 1
        # if isFound:
            # continue
        # i += 1
        # j += 1
        
    ############################### "Chet":
    if isChanged:
        #oppL = list(filter(lambda x: new_state[ x[0] ][ x[1] ] == oppColor, adjacentDict[index1]))
        if index1 % 2 != 0:
            # Only 1 case could happen to be "Chet" 
            yR = col1 - col0 + row1
            yC = row0 - row1 + col1
            zR = col0 - col1 + row1
            zC = row1 - row0 + col1
            if ( (0 <= yR < 5) and (0 <= yC < 5) and (new_state[yR][yC] != currColor) ):
                pass
            elif ( (0 <= zR < 5) and (0 <= zC < 5)  and (new_state[zR][zC] != currColor) ):
                pass
            else:
                for x in newOppL:
                    if traverse_CHET(x, currColor, oppColor, new_state):
                        isChanged = True
                    
        #elif index0 % 2 != 0:
        else:
            for x in newOppL:
                if traverse_CHET(x, currColor, oppColor, new_state):
                    isChanged = True
        
        for x in changedL:
            for y in adjacentDict[ x[0]*5 + x[1] ]:
                if (new_state[ y[0] ][ y[1] ] == oppColor) and ( traverse_CHET(y, currColor, oppColor, new_state) ):
                    isChanged = True
        
        
    else: # not "ganh" # isChanged == False
        if index1 % 2 != 0:
            # Only 1 case could happen to be "Chet" 
            yR = col1 - col0 + row1
            yC = row0 - row1 + col1
            zR = col0 - col1 + row1
            zC = row1 - row0 + col1
            if ( (0 <= yR < 5) and (0 <= yC < 5) and (new_state[yR][yC] != currColor) ):
                pass
            elif ( (0 <= zR < 5) and (0 <= zC < 5)  and (new_state[zR][zC] != currColor) ):
                pass
            else:
                for x in oppL:
                    if traverse_CHET(x, currColor, oppColor, new_state):
                        isChanged = True
                    
        #elif index0 % 2 != 0:
        else:
            for x in oppL:
                if traverse_CHET(x, currColor, oppColor, new_state):
                    isChanged = True
        #else: #(row0*5 + col0) % 2 == 0:
    
    # Check CH, check for each piece
    
    #traversedL = [pointList[0]]
    
    # while(True):
        
        # if (pointList[0][0] in evenL and pointList[0][1] in oddL) or (pointList[0][0] in oddL and pointList[0][1] in evenL):
            # pL = [(row1 - 1, col1), (row1, col1 - 1), (row1, col1 + 1), (row1 + 1, col1)]
        # pL = [(row1 - 1, col1 - 1), (row1 - 1, col1), (row1 - 1, col1 + 1), (row1, col1 - 1), (row1, col1 + 1), (row1 + 1, col1 - 1), (row1 + 1, col1), (row1 + 1, col1 + 1)]
    # else:
        
    
    # oppL = [] # list saving positions around the target point which have the opponent's chessmans
    # for x in pL:
        # if x[0] not in range(5) or x[1] not in range(5) or x == move[0] or state[x[0]][x[1]] == '.' or state[x[0]][x[1]] == state[row0][col0]:
            # continue
        # oppL.append(x)
    
    #*************************** Cuong's code **********************************
    # # Check CH,check for each piece
    # neighborPos = neighborPosDict[str(row*len(new_state)+col)]
    
    # # Get neighbor of "new move" piece
    # queue = []
    # for r,c in neighborPos:
        # if new_state[r][c] != new_state[row][col] and new_state[r][c] != '.':
            # queue.append((r,c))
    
    # # For each neighbor (it might "outside" or "inside" neighbor)
    # for e in queue:

        # adjPiece = []
        # chFlag = True
        # adjPiece.append(e)
        # #visitPiece = []
        # chPiece = []
        # temp_state = board_copy(new_state)
        
        # # Like BFS 
        # while adjPiece and chFlag:
            # #Get b to visit and mark it as visited,then pop it out from CHpiece
            # temp = adjPiece[0]
            # #visitPiece.append(temp)
            # adjPiece.pop(0)
        
            # #Get it neighbor
            # neighborPos = neighborPosDict[str(temp[0]*len(new_state)+temp[1])]
            # res = []
            # for r,c in neighborPos:
                # if new_state[r][c] == '.':
                    # res = []
                    # chFlag = False
                    # break
                # if new_state[r][c] != new_state[row][col]:
                    # res.append((r,c))
            
            # temp_state[temp[0]][temp[1]] = changePiece(temp_state[temp[0]][temp[1]])
            # adjPiece += res
        
        # if chFlag:
            # new_state = temp_state
            # break
        #***********************************************************************
    
    ################################ "Bay":
    if not isChanged: # this move didn't change any piece's color
        #TODO: check whether there is any trap created by this move. If yes, save that position.
        
        same0L = []
        isOppExist = False
        for x in adjacentDict[index0]:
            if new_state[ x[0] ][ x[1] ] == currColor:
                same0L.append(x)
            elif new_state[ x[0] ][ x[1] ] == oppColor:
                isOppExist = True
        
        if isOppExist: # if exist an opponent which can reach that position
            isOppExist = False
            for x in same0L:
                yR = row0*2 - x[0]
                yC = col0*2 - x[1]
                if (0 <= yR < 5) and (0 <= yC < 5) and ( new_state[ yR ][ yC ] == currColor ):
                    a[-1].append( move[0] )
                    break
        
        #sameL = list(filter(lambda x: new_state[ x[0] ][ x[1] ] == currColor, adjacentDict[index0]))
        
        # for x in adjacentDict[index0]:
            # if new_state[ x[0] ][ x[1] ] == currColor:
                # yR = row0*2 - x[0]
                # yC = col0*2 - x[1]
                # if (0 <= yR < 5) and (0 <= yC < 5) and ( new_state[ yR ][ yC ] == currColor ):

                    # a[-1].append( move[0] )
                    # break
        
        # isOppExist == False
        for x in pointL: # excluded move[0]
            for y in adjacentDict[ x[0]*5 + x[1] ]:
                if new_state[ y[0] ][ y[1] ] == oppColor:
                    isOppExist = True
                    break
            
            if isOppExist:
                isOppExist = False
                yR = x[0]*2 - row1
                yC = x[1]*2 - col1
                if (0 <= yR < 5) and (0 <= yC < 5) and ( new_state[ yR ][ yC ] == currColor ):
                    a[-1].append( x )
    
    #else:# some chessman has color changed, check trapped turn finishment
        # if a[-1]: # trapped turn
            # a[-1] = [] # no need of these traps
        #else: not a trapped turn
        #do nothing
        
    ########################################
    
    #new_state = board_copy(state)
    return new_state

#======================================================================
Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]

# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
#======================================================================


def play(student_a, student_b, start_state=Initial_Board):
    player_a = imp.load_source(student_a, student_a + ".py")
    player_b = imp.load_source(student_b, student_b + ".py")

    a = player_a.Player('b')
    b = player_b.Player('r')
    
    curr_player = a
    state = start_state

    board_num = 0
    
    board_print(state)
    
    prevList = [curr_player, board_num]
    while True:
        print("It is " + str(curr_player) + "'s turn.")
        
        copyState = board_copy(state)
        
        start = time.time()
        move = curr_player.next_move(copyState)
        elapse = time.time() - start

        # print(move)
        
        #TODO: need to check more to figuring out if student return the correct format of a move
        if not move or len(move) < 2: # move is empty or some other cases
            break
        
        print("The move is:", move, end=" ")
        print("(in %.2f ms)" % (elapse*1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        print()
        # check_move ???
        state = doit(move, state, prevList)
        if state is None:
            break
        
        board_num += 1
        board_print(state, num=board_num)
        if board_num == 88:
            print("ahihi")
        if curr_player == a:
            curr_player = b
        else:
            curr_player = a
            
        prevList[0] = curr_player
        prevList[1] = board_num

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')

play("1652192", "1652192")
