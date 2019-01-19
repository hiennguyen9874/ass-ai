
import imp
import time
#======================================================================


def board_print(board, move=[], num=0):

    print("====== The current board(", num, ")is (after move): ======")
    if move:
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
# Student SHOULD implement this function to change current state to new state properly
def doit(move, state):
    new_state = board_copy(state)
    if not move or not state:
        return None
    #else:
    if move[0] == move[1]:
        return None
    
    row1 = move[0][0]
    col1 = move[0][1]
    row2 = move[1][0]
    col2 = move[1][1]

    ta = state[row1][col1]
    dich = None
    if ta == 'r':
        dich = 'b'
    else:
        dich = 'r'

    new_state[row2][col2] = ta
    new_state[row1][col1] = '.'

    move = row2*5 + col2
    lst = list()
    if move % 2 == 0:
        lst = [(move - 6, move + 6), (move - 5, move + 5), (move - 4, move + 4), (move - 1, move + 1)]
    else:
        lst = [(move - 5, move + 5), (move - 1, move + 1)]
    for x in lst:
        if x[0] >= 0 and x[0] <= 24 and x[0] % 5 - col2 in [-1, 0, 1] and x[1] >= 0 and x[1] <= 24 and x[1] % 5 - col2 in [-1, 0, 1]:
            r1 = int(x[0]/5)
            c1 = x[0] % 5
            r2 = int(x[1]/5)
            c2 = x[1] % 5
            if new_state[r1][c1] == dich and new_state[r2][c2] == dich:
                new_state[r1][c1] = ta
                new_state[r2][c2] = ta

    lst_dich = list()
    for i in range(5):
        for j in range(5):
            if new_state[i][j] == dich:
                lst_dich.append([i, j, False])

    def lien_ke(i, j, i1, j1):
        lst = list()
        k = i * 5 + j
        if k % 2 == 0:
            lst = [k-6, k-5, k-4, k-1, k+1, k+4, k+5, k+6]
        else:
            lst = [k-5, k-1, k+1, k+5]
        if j1 - i1 in [-1, 0, 1] and i1*5+j1 in lst:
            return True
        return False

    list_dich = list()
    for i in range(5):
        for j in range(5):
            if new_state[i][j] == dich:
                list_dich.append([i, j, False])

    def traverse_CHET(startPos, currColor, oppColor, state, q = []):
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

    for i in range(5):
        for j in range(5):
            if new_state[i][j] == dich:
                traverse_CHET((i, j), ta, dich, new_state)
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
    
    while True:
        print("It is ", curr_player, "'s turn")

        start = time.time()
        move = curr_player.next_move(state)
        # move = [(4, 2), (3, 2)]
        elapse = time.time() - start

        # print(move)

        if not move:
            break

        print("The move is : ", move, end=" ")
        print(" (in %.2f ms)" % (elapse*1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        print()
        # check_move
        state = doit(move, state)

        board_num += 1
        board_print(state, num=board_num)

        if curr_player == a:
            curr_player = b
        else:
            curr_player = a

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')

play("1652192", "1652192")