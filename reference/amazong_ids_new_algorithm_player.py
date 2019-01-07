import time
class Player:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    def find_best_move(self, state):
        self.best_path = []
        self.max_depth = 1
        self.max_depth_reached = 0
        self.start_time = time.time()
        self.max_time = 2.8
        self.visited = 0
        self.num_move = 0
        self.num_cut_off = 0
        self.is_time_out = False
        self.root_state = state

        alpha = -10000
        beta = 10000
        color = 1
        depth = 0

        # movements1 = self.game.get_all_moves(state, self.str)
        # print(len(movements1))
        current_node = Node(state, None, None, 0, None)
        movements = self.game.get_all_moves(current_node.state, self.str)
        num_of_moves = len(movements)

        # if AI move first, do sample move
        sample_move_w = [(0, 3), (7, 3), (5, 1)]

        if num_of_moves == 2176:
            return sample_move_w

        # if can't move => lose
        if num_of_moves == 0:
            return None

        best_score = -10000
        # best_child = None
        while not self.time_out():
            for movement in movements:
                if self.time_out():
                    self.is_time_out = True
                    break
                new_state = self.game.move(movement, current_node.state)
                child = Node(new_state, movement, None, depth + 1, None)
                score = -self.negamax(child, depth + 1, -beta, -alpha, -color)
                child.score = score
                if not self.is_time_out:
                    if score > best_score:
                        best_score = score
                        current_node.best_child = child
                    alpha = max(alpha, score)
                if alpha >= beta:
                    self.num_cut_off += 1
                    best_score = alpha

            self.max_depth += 1

        if current_node.best_child is None:
            return None

        print("visited: %d/%d node(s) - num first move: %d" % (self.visited, num_of_moves, self.num_move))
        print("cut-off: %d time(s)" % self.num_cut_off)
        node = current_node
        while node is not None:
            print("Depth - Move - Score:", node.depth, node.movement, node.score)
            node = node.best_child
        print("best score:", current_node.best_child.score)
        return current_node.best_child.movement

    # For concurrent version (not implement yet)
    def get_child(self, movement):
        alpha = -10000
        beta = 10000
        color = 1
        depth = 0
        new_state = self.game.move(movement, self.root_state)
        child = Node(new_state, movement, None, depth + 1, None)
        score = -self.negamax(child, depth + 1, -beta, -alpha, -color)
        child.score = score
        return child

    def negamax(self, node, depth, alpha, beta, color):
        player = self.str
        opponent = self.game.get_opponent(player)
        self.max_depth_reached = max(depth, self.max_depth_reached)
        self.visited += 1

        # print("Start search at depth:", depth)
        # print("Movement to reach here is:", node.movement)
        movements = None
        if self.is_player_turn(color):
            movements = self.game.get_all_moves(node.state, player)
        else:
            movements = self.game.get_all_moves(node.state, opponent)
        score = self.evaluate_function(node.state, player, len(movements))

        # check game over
        if self.is_player_turn(color):
            if self.player_lose(color, score):
                return self.evaluator.LOSE_SCORE * color
            movements = self.game.get_all_moves(node.state, player)
            if self.player_win(color, score):
                if len(movements) == 0:
                    raise RuntimeError("WTF, player not lose but can't move???")
                movement = movements[0]
                new_state = self.game.move(movement, node.state)
                node.best_child = Node(new_state, movement, score * color, depth + 1, None)
                return self.evaluator.WIN_SCORE * color
        else:
            if self.player_win(color, score):
                return self.evaluator.WIN_SCORE * color
            movements = self.game.get_all_moves(node.state, opponent)
            if self.player_lose(color, score):
                if len(movements) == 0:
                    raise RuntimeError("WTF, player not lose but can't move???")
                movement = movements[0]
                new_state = self.game.move(movement, node.state)
                node.best_child = Node(new_state, movement, score * color, depth + 1, None)
                return self.evaluator.LOSE_SCORE * color

        # check limit
        if self.reach_max_depth(depth):
            return score * color

        if self.time_out():
            # print("Reach limit")
            # print("Depth %d score %d" % (depth, score * color))
            self.is_time_out = True
            return score * color

        best_score = -10000
        for movement in movements:
            new_state = self.game.move(movement, node.state)
            child = Node(new_state, movement, None, depth + 1, None)
            score = -self.negamax(child, depth + 1, -beta, -alpha, -color)
            # print("Alpha %d - Beta %d - Score %d" % (alpha, beta, score))
            child.score = score
            if score > best_score:
                best_score = score
                node.best_child = child
                if len(self.best_path) <= node.best_child.depth:
                    self.best_path.append(node.best_child)
                else:
                    self.best_path[node.best_child.depth] = node.best_child
                # print("Alpha changed")
            alpha = max(alpha, score)
            if alpha >= beta:
                # print("alpha: %d >= beta: %d => cut off" % (alpha, beta))
                self.num_cut_off += 1
                return alpha
            if self.time_out():
                self.is_time_out = True
                break
        # print("Depth %d score %d" % (depth, best_score))
        # print("Movement chose:", node.best_child)
        # print("Alpha %d - Beta %d - Best score %d" % (alpha, beta, best_score))
        # if (alpha != best_score):
        #     raise RuntimeError("Alpha not equal with best score", alpha, best_score)
        return best_score

    def is_player_turn(self, color):
        return color > 0

    def time_out(self):
        return time.time() - self.start_time >= self.max_time

    def reach_max_depth(self, depth):
        return depth >= self.max_depth

    def player_win(self, color, score):
        '''
        player win in 2 cases:
            Both can't move and is opponent turn
            Player can move, but opponent can't
        '''
        if score == self.evaluator.NO_MOVE_SCORE:
            return not self.is_player_turn(color)
        return score == self.evaluator.WIN_SCORE

    def player_lose(self, color, score):
        '''
        player lose in 2 cases:
            Both can't move and is player turn
            Player can't move, but opponent can
        '''
        if score == self.evaluator.NO_MOVE_SCORE:
            return self.is_player_turn(color)
        return score == self.evaluator.LOSE_SCORE

    def nextMove(self, state):
        self.game = Amazons(len(state))
        self.evaluator = AmazonsEvaluator(self.game)
        self.evaluate_function = self.evaluator.evaluate_by_amazong_method
        movement = self.find_best_move(state)
        return movement

class AmazonsEvaluator:
    def __init__(self, game):
        self.game = game
        self.WIN_SCORE = 1000
        self.LOSE_SCORE = -1000
        self.NO_MOVE_SCORE = 2000

    # =========== amazong method ==============
    def evaluate_by_amazong_method(self, board, player, num_all_moves):
        # get necessary resources
        (white_locations, black_locations, shot_cells, empty_cells) \
            = self.calculate_locations(board)

        white_q_territory, white_mobility, black_q_territory, black_mobility, \
        neutral_q_territory, devided \
            = self.count_territory_by_queen_distance(white_locations, black_locations, empty_cells, board)
        white_queen_territory = (white_q_territory - black_q_territory) \
                                - 0.2 * neutral_q_territory
        black_queen_territory = -0.4 * neutral_q_territory - white_queen_territory

        white_k_territory, black_k_territory, neutral_k_territory\
            = self.count_territory_by_king_distance(white_locations, black_locations, empty_cells, board)
        white_king_territory = (white_k_territory - black_k_territory) \
                               - 0.2 * neutral_k_territory
        black_king_territory = -0.4 * neutral_k_territory - white_king_territory

        # both player can't move
        if white_mobility + black_mobility == 0:
            return self.NO_MOVE_SCORE

        # if the map is totally separated, dont need t2 any more
        if devided:
            white_king_territory = 0

        if player == 'w':
            if white_mobility == 0:
                return self.LOSE_SCORE
            if black_mobility == 0:
                return self.WIN_SCORE

            if num_all_moves > 1000:
                return 0.2 * white_queen_territory + 0.8 * white_king_territory
            elif num_all_moves > 200:
                return 0.5 * white_queen_territory + 0.5 * white_king_territory
            else:
                return 0.8 * white_queen_territory + 0.2 * white_king_territory
        else:
            if black_mobility == 0:
                return self.LOSE_SCORE
            if white_mobility == 0:
                return self.WIN_SCORE

            if num_all_moves > 1000:
                return 0.2 * black_queen_territory + 0.8 * black_king_territory
            elif num_all_moves > 200:
                return 0.5 * black_queen_territory + 0.5 * black_king_territory
            else:
                return 0.8 * black_queen_territory + 0.2 * black_king_territory

    def count_territory_by_queen_distance(self, white_locations, black_locations, empty_cells, board):
        # initial set of unmark_cells
        unmark_cells = empty_cells.copy()

        # STEP 1

        # mark all location that white queen can move directly
        white_cells = set()
        for queen_location in white_locations:
            white_cells |= self.game.get_valid_queen_moves(queen_location, board)

        # mark all location that black queen can move directly
        black_cells = set()
        for queen_location in black_locations:
            black_cells |= self.game.get_valid_queen_moves(queen_location, board)

        # get mobility of both player
        white_mobility = len(white_cells)
        black_mobility = len(black_cells)

        # neutral contain cells that marked by both white and black
        neutral_cells = white_cells & black_cells

        # can reach cells to determine cells player can reach
        # white_can_reach = set()
        # black_can_reach = set()

        # remove marked cells from unmark_cells set
        unmark_cells = unmark_cells - white_cells - black_cells - neutral_cells

        # STEP 2
        i = 0
        while True:
            i += 1
            if len(unmark_cells) == 0: break

            temp_white_cells = set()
            temp_black_cells = set()
            for cell in unmark_cells:
                can_reach_cells = self.game.get_valid_queen_moves(cell, board)
                if len(can_reach_cells & white_cells) > 0:
                    temp_white_cells.add(cell)
                if len(can_reach_cells & black_cells) > 0:
                    temp_black_cells.add(cell)
                # if len(can_reach_cells & white_can_reach) > 0:
                #     white_can_reach.add(cell)
                # if len(can_reach_cells & black_can_reach) > 0:
                #     black_can_reach.add(cell)

            unmark_cells = unmark_cells - temp_white_cells - temp_black_cells

            temp_neutral_cells = temp_white_cells & temp_black_cells

            white_cells |= temp_white_cells
            black_cells |= temp_black_cells
            neutral_cells |= temp_neutral_cells

            has_newly_marked_cell = (len(temp_white_cells) + len(temp_black_cells) > 0)
            if not has_newly_marked_cell: break
        white_cells -= neutral_cells
        black_cells -= neutral_cells

        white_territory = len(white_cells)
        neutral_territory = len(neutral_cells)
        black_territory = len(black_cells)

        devided = False
        if neutral_territory == 0:
            devided = True

        return white_territory, white_mobility, black_territory, black_mobility, \
               neutral_territory, devided

    def count_territory_by_king_distance(self, white_locations, black_locations, empty_cells, board):
        unmark_cells = empty_cells.copy()

        # mark all location that white queen can move directly
        white_cells = set()
        for queen_location in white_locations:
            white_cells |= self.get_valid_king_moves(queen_location, board)

        # mark all location that black queen can move directly
        black_cells = set()
        for queen_location in black_locations:
            black_cells |= self.get_valid_king_moves(queen_location, board)

        # neutral contain cells that marked by both white and black
        neutral_cells = white_cells & black_cells

        # can reach cells to determine cells player can reach
        # white_can_reach = set()
        # black_can_reach = set()

        # remove marked cells from unmark_cells set
        marked_cells = white_cells | black_cells | neutral_cells
        unmark_cells -= marked_cells

        while True:
            if len(unmark_cells) == 0: break
            temp_white_cells = set()
            temp_black_cells = set()

            for cell in white_cells:
                temp_white_cells |= self.get_valid_king_moves(cell, board)
                temp_white_cells -= marked_cells

            for cell in black_cells:
                temp_black_cells |= self.get_valid_king_moves(cell, board)
                temp_black_cells -= marked_cells

            # white_can_reach |= temp_white_cells
            # black_can_reach |= temp_black_cells

            temp_neutral_cells = temp_white_cells & temp_black_cells
            temp_marked_cells = temp_white_cells | temp_black_cells

            marked_cells |= temp_marked_cells
            unmark_cells -= temp_marked_cells

            white_cells |= temp_white_cells
            black_cells |= temp_black_cells
            neutral_cells |= temp_neutral_cells

            has_newly_marked_cell = len(temp_marked_cells)
            if not has_newly_marked_cell: break

        white_cells -= neutral_cells
        black_cells -= neutral_cells

        neutral_territory = len(neutral_cells)
        white_territory = len(white_cells)
        black_territory = len(black_cells)
        # white_reach = len(white_can_reach - black_can_reach)
        # black_reach = len(black_can_reach - white_can_reach)

        return white_territory, black_territory, neutral_territory

    def get_valid_king_moves(self, king_location, board):
        (row, col) = king_location
        return set([
            (i, j)
            for i in range(row - 1, row + 2)
            for j in range(col - 1, col + 2)
            if (i >= 0 and i < len(board))
               and (j >= 0 and j < len(board))
               and (board[i][j] == '.')
        ])

    def calculate_mobility(self, board):
        (white_queen_locations, black_queen_locations, shot_cells, empty_cells) \
        = self.calculate_locations(board)

        # get cells that white can directly move to
        white_cells = set()
        for queen_location in white_queen_locations:
            white_cells |= self.game.get_valid_queen_moves(queen_location, board)
        # get cells that black can directly move to
        black_cells = set()
        for queen_location in black_queen_locations:
            black_cells |= self.game.get_valid_queen_moves(queen_location, board)

        return len(white_cells), len(black_cells)

    def calculate_locations(self, board):
        white_locations = set()
        black_locations = set()
        shooted_cells = set()
        empty_cells = set()
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                cell = board[row][col]
                if cell == 'w':
                    white_locations.add((row,col))
                elif cell == 'b':
                    black_locations.add((row,col))
                elif cell == 'X':
                    shooted_cells.add((row,col))
                elif cell == '.':
                    empty_cells.add((row, col))
                else:
                    raise RuntimeError("Cell [%d][%d] is invalid" % (row,col))

        return (white_locations, black_locations, shooted_cells, empty_cells)

class Node:
    def __init__(self, state, movement, score, depth, best_child):
        self.state = state
        self.movement = movement
        self.score = score
        self.depth = depth
        self.best_child = best_child

    def __str__(self):
        return str(self.movement)

    def __lt__(self, other):
        if self.depth != other.depth:
            raise RuntimeError("Cannot compare 2 nodes in different depth")
        if self.depth % 2 == 1:
            return self.score < other.score
        else:
            return self.score > other.score

class Amazons:
    def __init__(self, board_size=10):
        self.initial_board = AmazonsBoardGenerator.generate_board(board_size)
        self.board_size = board_size

    def is_valid_move(self, movement, board):
        """
        Check the validity of the movement

        Parameters:
        ----------

        movement: list of [old_location, new_location, shot_cell]
            old_location: the current location of the queen the will be moved
            new_location: the location the the queen will be moved to
            shot_cell: the cell will be shot after move the queen

        board: matrix
            the current board

        Returns:
        ----------
        validity: boolean
           False if meet 1 of these following rules:
                - old_location not contain a queen
                - new_location not in set of cell that the queen can move to
                - shot_cell not in set of cell thet the queen can shoot after move

            True in other conditions
        """
        # print(self.board_size)
        old_location = movement[0]
        new_location = movement[1]
        shot_cell = movement[2]

        # old_location not contain any queen
        (old_row, old_col) = old_location
        if (board[old_row][old_col] != 'b' and
                board[old_row][old_col] != 'w'):
            print("There aren't any queen to move")
            return False

        # new location is not in set of valid move of old location
        valid_moves = self.get_valid_queen_moves(old_location, board)
        if new_location not in valid_moves:
            print("Move to invalid location")
            return False

        # shot cell is not in set of valid shot of new location
        new_board = self.move_queen(old_location, new_location, board)
        valid_shots = self.get_valid_queen_shoots(new_location, new_board)
        if shot_cell not in valid_shots:
            print("Shoot to invalid location")
            return False

        return True

    # ========== Heuristic score ==========
    def evaluate_score(self):
        pass

    # ========== Get movements ==========
    def get_all_ordered_moves_with_score(self, board, player, evaluate_function):
        """
        Get all the valid movements of given player on given board
            Get all queen locations of given player
            For each queen, get all possible new locations that the queen can move to
                For each new location, get all possible cell locations that the queen can shoot
                A movement is a combination of: [old_location, new_location, shot_cell]
                Append the movement to the list of movements

        Parameters:
        ----------

        board: matrix
            the current board
        player: string 'w' or 'b'
            the player who move this turn

        Returns:
        list of all valid movements: list
            The list of all valid movements for all 4 queens of the given player
        """

        queen_locations = set([(row, col)
                               for row in range(self.board_size)
                               for col in range(self.board_size)
                               if board[row][col] == player])
        movements_with_score = []
        for queen_location in queen_locations:
            new_locations = self.get_valid_queen_moves(queen_location, board)
            for new_location in new_locations:
                new_board = self.move_queen(queen_location, new_location, board)
                shot_cells = self.get_valid_queen_shoots(new_location, new_board)
                for shot_cell in shot_cells:
                    movement = [queen_location, new_location, shot_cell]
                    new_board = self.move(movement, board)
                    score = evaluate_function(new_board, player)
                    # negative score for max heap
                    heapq.heappush(movements_with_score, (-score, movement))

        return movements_with_score

    def get_all_moves(self, board, player):
        """
        Get all the valid movements of given player on given board
            Get all queen locations of given player
            For each queen, get all possible new locations that the queen can move to
                For each new location, get all possible cell locations that the queen can shoot
                A movement is a combination of: [old_location, new_location, shot_cell]
                Append the movement to the list of movements

        Parameters:
        ----------

        board: matrix
            the current board
        player: string 'w' or 'b'
            the player who move this turn

        Returns:
        list of all valid movements: list
            The list of all valid movements for all 4 queens of the given player
        """

        queen_locations = set([(row, col)
                               for row in range(self.board_size)
                               for col in range(self.board_size)
                               if board[row][col] == player])
        movements = []
        for queen_location in queen_locations:
            new_locations = self.get_valid_queen_moves(queen_location, board)
            for new_location in new_locations:
                new_board = self.move_queen(queen_location, new_location, board)
                shot_cells = self.get_valid_queen_shoots(new_location, new_board)
                for shot_cell in shot_cells:
                    movement = [queen_location, new_location, shot_cell]
                    movements.append(movement)

        return movements

    def get_valid_queen_moves(self, queen_location, board):
        """
        Parameter:
        ----------
        queen_location: tuple (row, col)
            the location of the queen is about to be move
        board: matrix
            the current board

        Returns:
        ----------
        set of queen's movement: set
            Set of all location that the chosen queen can be move to
            Queen can move orthogonally or diagonally
            Queen cannot move through impediment (other queens, shot cells)
        """
        movements = self.get_valid_horizontal_moves(queen_location, board) \
                    | self.get_valid_vertical_moves(queen_location, board) \
                    | self.get_valid_diagonal_moves(queen_location, board)
        return movements

    def get_valid_queen_shoots(self, queen_location, board):
        """
        The same with the function get_valid_queen_moves
        Because shoot rules is the same with move rules
        """

        return self.get_valid_queen_moves(queen_location, board)

    def get_valid_horizontal_moves(self, queen_location, board):
        """
        left and right
        """
        movements = set()
        # left
        (row, col) = queen_location
        col -= 1
        while col >= 0 and board[row][col] == '.':
            movements.add((row, col))
            col -= 1
        # right
        (row, col) = queen_location
        col += 1
        while col < self.board_size and board[row][col] == '.':
            movements.add((row, col))
            col += 1

        return movements

    def get_valid_vertical_moves(self, queen_location, board):
        """
        up and down
        """
        movements = set()
        # up
        (row, col) = queen_location
        row -= 1
        while row >= 0 and board[row][col] == '.':
            movements.add((row, col))
            row -= 1
        # down
        (row, col) = queen_location
        row += 1
        while row < self.board_size and board[row][col] == '.':
            movements.add((row, col))
            row += 1

        return movements

    def get_valid_diagonal_moves(self, queen_location, board):
        """
        4 directions of a diagonal
        """
        movements = set()
        # (0,0) -> (9,9)
        (row, col) = queen_location
        row += 1
        col += 1
        while row < self.board_size and col < self.board_size and board[row][col] == '.':
            movements.add((row, col))
            row += 1
            col += 1
        # (9,9) -> (0,0)
        (row, col) = queen_location
        row -= 1
        col -= 1
        while row >= 0 and col >= 0 and board[row][col] == '.':
            movements.add((row, col))
            row -= 1
            col -= 1
        # (0,9) -> (9,0)
        (row, col) = queen_location
        row += 1
        col -= 1
        while row < self.board_size and col >= 0 and board[row][col] == '.':
            movements.add((row, col))
            row += 1
            col -= 1
        # (9,0) -> (0,9)
        (row, col) = queen_location
        row -= 1
        col += 1
        while row >= 0 and col < self.board_size and board[row][col] == '.':
            movements.add((row, col))
            row -= 1
            col += 1

        return movements

    def can_move(self, board, player):
        """
        Check if the given player can keep moving
        """
        return len(self.get_all_moves(board, player)) > 0

    # ========== Make the movement ==========
    def move(self, movement, board):
        """
        Make a complete movement include 2 step:
            step 1: move the queen
            step 2: shoot
        """
        if not self.is_valid_move(movement, board):
            raise RuntimeError("Invalid movement")

        old_location = movement[0]
        new_location = movement[1]
        shot_cell = movement[2]
        new_board = self.move_queen(old_location, new_location, board)
        new_board = self.shoot(shot_cell, new_board)
        return new_board

    def move_queen(self, old_location, new_location, board):
        """
        Only move the queen to new location

        Parameters:
        ----------
        old_location: tuple(row,col)
            the current queen location
        new_location: tuple(row,col)
            the cell that the queen will move to

        Returns:
        ----------
        new board: matrix
            new board after the queen move

        Exceptions:
        ----------
        RuntimeError:
            if old_location is not has any queen
        """
        new_board = self.copy_board(board)
        (old_row, old_col) = old_location
        (new_row, new_col) = new_location
        if board[old_row][old_col] == 'w':
            new_board[new_row][new_col] = 'w'
        elif board[old_row][old_col] == 'b':
            new_board[new_row][new_col] = 'b'
        else:
            raise RuntimeError("There aren't any queen to move")
        new_board[old_row][old_col] = '.'
        return new_board

    def shoot(self, shot_cell, board):
        """
        Only make the shoot

        Parameters:
        ----------
        shot_cell: tuple(row,col)
            the cell will be shot

        Returns:
        ----------
        new board: matrix
            new board after shoot
        """
        new_board = self.copy_board(board)
        new_board[shot_cell[0]][shot_cell[1]] = 'X'
        return new_board

    # ========== Util functions ==========
    def copy_board(self, board):
        new_board = [[]] * self.board_size
        for i in range(self.board_size):
            new_board[i] = [] + board[i]
        return new_board

    def print_board(self, board):
        board_size = len(board)
        for i in range(board_size - 1, -1, -1):
            print(i, ":", end=" ")
            for j in range(board_size):
                print(board[i][j], end=" ")
            print()
        print("   ", *list(range(board_size)))
        print()

    def get_opponent(self, player):
        if player == 'w':
            return 'b'
        elif player == 'b':
            return 'w'
        else:
            raise RuntimeError('Invalid player')

class AmazonsBoardGenerator:
    @staticmethod
    def generate_board(board_size):
        return {
            2   : AmazonsBoardGenerator.generate_board_2,
            3   : AmazonsBoardGenerator.generate_board_3,
            4   : AmazonsBoardGenerator.generate_board_4,
            5   : AmazonsBoardGenerator.generate_board_5,
            6   : AmazonsBoardGenerator.generate_board_6,
            7   : AmazonsBoardGenerator.generate_board_7,
            8   : AmazonsBoardGenerator.generate_board_8,
            # 9   : AmazonsBoardGenerator.generate_board_9,
            10  : AmazonsBoardGenerator.generate_board_10
        }[board_size]()

    @staticmethod
    def generate_board_2():
        return [
            ['w', '.'],
            ['.', 'b'],
        ]

    @staticmethod
    def generate_board_3():
        return [
            ['w', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', 'b'],
        ]

    @staticmethod
    def generate_board_4():
        return [
            ['w', '.', '.', 'w'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['b', '.', '.', 'b'],
        ]

    @staticmethod
    def generate_board_5():
        return [
            ['.', 'w', '.', 'w', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', 'b', '.', 'b', '.'],
        ]

    @staticmethod
    def generate_board_6():
        return [
            ['.', 'w', '.', '.', 'w', '.'],
            ['w', '.', '.', '.', '.', 'w'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', 'b'],
            ['.', 'b', '.', '.', 'b', '.'],
        ]

    @staticmethod
    def generate_board_7():
        return [
            ['.', '.', 'w', '.', 'w', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['w', '.', '.', '.', '.', '.', 'w'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', 'b'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'b', '.', 'b', '.', '.'],
        ]

    @staticmethod
    def generate_board_8():
        return [
            ['.', '.', 'w', '.', '.', 'w', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['w', '.', '.', '.', '.', '.', '.', 'w'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', '.', 'b'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'b', '.', '.', 'b', '.', '.'],
        ]

    @staticmethod
    def generate_board_10():
        return [
            ['.', '.', '.', 'w', '.', '.', 'w', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['w', '.', '.', '.', '.', '.', '.', '.', '.', 'w'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', '.', '.', '.', 'b'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'b', '.', '.', 'b', '.', '.', '.'],
        ]

if __name__ == '__main__':
    game = Amazons(10)
    game.print_board(game.initial_board)