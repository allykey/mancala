import termcolor
from termcolor import colored, cprint
import random
import copy
import time

# == Mancala ==================================================================

class Board:
    player_to_background = {"A": "on_red", "B": "on_blue"}

    def __init__(self):
        # start with B (user), then A (computer)
        # stores initially have 0 seeds
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.extra_move = None
        self.current_capture = None

    def gets_extra_move(self):
        return self.extra_move
    
    def tally_up(self):
        store_counts = self.get_store_counts()
        b_score = store_counts['B'] + self.get_player_seeds('B')
        a_score = store_counts['A'] + self.get_player_seeds('A')

        return {'B': b_score, 'A': a_score}

    def get_legal_actions(self, player):
        start = 0
        end = 6
        if player == 'A':
            start = 7
            end = 13

        legal_actions = []

        # consider all of player's available pits (excluding store)
        for i in range(start, end):
            # skip empty pits
            if self.get_pit_seeds(i) == 0:
                continue 
            legal_actions.append(i)

        return legal_actions

    # get the seed count in a single specified pit
    def get_pit_seeds(self, pit_num):
        if not (0 <= pit_num <= 5) and not (7 <= pit_num <= 12):
            return -1
        return self.board[pit_num]
    
    # only does this for player's own pits
    def perf_dist_from_store(self, player):
        # default to player B (user)
        start = 0
        end = 6 
        if player == 'A':
            start = 7
            end = 13

        # calculate distances from player's pits to store (excluding store)
        for i in range(start, end):
            dist = self.get_dist_from_store(i, player)
            if (self.get_pit_seeds(i) == dist):
                return True
            
        return False

    # does not consider pits from opponent's side
    def get_dist_from_store(self, pit_num, player):
        if player == 'A':
            return 13 - pit_num
        if player == 'B':
            return 6 - pit_num
    
    def get_store_counts(self):
        return {"A": self.board[13], "B": self.board[6]}
        
    def move_seeds(self, pit_num, player):
        i = pit_num

        # get number of seeds in pit
        num_seeds = self.board[i]

        # empty specified pit
        self.board[i] = 0

        # distribute seeds counter-clockwise
        while num_seeds > 0:
            i = (i + 1) % len(self.board)

            # skip opponent's store (home)
            if player == 'B' and i == 13:
                continue
            elif player == 'A' and i == 6:
                continue

            self.board[i] += 1
            num_seeds -= 1

        # if last seed lands in pit, active player gets an extra turn
        if (player == 'B' and i == 6):
            self.extra_move = 'B'
        elif (player == 'A' and i == 13):
            self.extra_move = 'A'
        else:
            self.extra_move = None

        # ACCOUNT FOR CAPTURES
        capture_occurred = False
        if self.get_pit_seeds(i) == 1:
            # check if seed landed on own side
            if (player == 'B' and 0 <= i <= 5) or (player == 'A' and 7 <= i <= 12):
                # check if opposite pit has seeds
                if self.get_pit_seeds(12 - i) > 0:
                    self.current_capture = (player, i, 12 - i)
                    capture_occurred = True
        if not capture_occurred:
            self.current_capture = None

    def get_capture(self):
        return self.current_capture
    
    # assumes self.current_capture has been set correctly
    def perform_capture(self):
        # unpack capture tuple
        capturing_player, capturing_pit, captured_pit = self.current_capture

        # determine store index based on player
        store = 6
        if capturing_player == 'A':
            store = 13
        
        # move pit seeds to store
        self.board[store] = self.board[store] + self.board[capturing_pit] + self.board[captured_pit]

        # empty relevant pits
        self.board[capturing_pit] = 0
        self.board[captured_pit] = 0
        return
            
    # excluding store seeds, get the sum of seeds in all pits associated with
    # one player
    def get_player_seeds(self, player):
        score = 0

        # for user
        start = 0
        end = 6

        # for computer
        if player == 'A':
            start = 7
            end = 13

        for i in range(start, end):
            score += self.board[i]

        return score
    
    # Returns true when either player has no seeds on their side
    def at_terminal_state(self):
        status = self.players_done()
        return status[0] or status[1]
    
    def players_done(self):
        userDone = True

        # up to user's store
        for i in range(6):
            if self.board[i] != 0:
                userDone = False
                break

        # up to computer's store
        computerDone = True
        for i in range(7, 13):
            # TESTING
            # print(f"at {i}: {self.board[i]}")
            if self.board[i] != 0:
                computerDone = False
                break

        # TESTING
        # print(f"userDone: {userDone}, computerDone: {computerDone}")

        return (userDone, computerDone)

    def print_pit(self, num_seeds, player):
        # padding: should add up to exactly 4 spaces when printed with num_seeds
        padding = "".join((4 - len(str(num_seeds))) * [" "])

        cprint(f'{num_seeds}{padding}',
            "white",
            self.player_to_background[player],
            end="")
        
        # add white space between each pit, and prevent newline
        print(" ", end="") 

    # so we can align A and B's pits with each other on different lines
    def print_empty_home(self, player):
        cprint('    ',
            "white",
            self.player_to_background[player],
            attrs=['bold'],
            end="")
        print(" ", end="")


    def print_home(self, num_seeds, player):
        # again, total space alloted to printing should be 4 spaces
        padding = "".join((4 - len(str(num_seeds))) * [" "])
        cprint(f'{num_seeds}{padding}',
            "white",
            self.player_to_background[player],
            attrs=['bold'],
            end="")
        print(" ", end="")


    def print_board(self):
        self.print_home(self.board[len(self.board) - 1], 'A')
        for pit in reversed(self.board[7:len(self.board) - 1]):
            self.print_pit(pit, 'A')
        self.print_home(self.board[6], 'B')
        print()
        self.print_empty_home('A')
        for pit in (self.board[0:6]):
            self.print_pit(pit, 'B')
        self.print_empty_home('B')
        print()    

class Agent:
    def __init__(self, depth, side, opponent_side):
        # cutoff depth for minimaxing
        self.depth = depth
        self.side = side
        self.opponent_side = opponent_side
        

    def get_next_action(self, board: Board):
        # TESTING
        return self.get_next_action_research(board)
    
        # start from computer's maximizing point of view
        tree_level = 0
        utility, action = self.max_value(board, tree_level, float('-inf'), float('inf'))
        return action

    # return estimated next best action for player
    def get_next_action_research(self, board: Board):
        # tree_level = 0
        # best_value = float('-inf')
        # best_action = None
        # for action in board.get_legal_actions(self.side):
        #     board_copy = copy.deepcopy(board)
        #     board_copy.move_seeds(action, self.side)
        #     value = self.standard_minimax(self.side, board_copy, float('-inf'), float('inf'), tree_level)
        #     if value > best_value:
        #         best_action = action
        
        # return best_action

        # return self.standard_minimax(self.side, board, float('-inf'), float('inf'), 0)["action"]
    
        return self.modified_minimax(self.side, board, float('-inf'), float('inf'), 0)

    # heuristic for getting utility of state
    def eval_func(self, board: Board):
        # TESTING
        # print(f"{board.get_store_counts()['A']}")

        # good: put seed in store
        # store_count = board.get_store_counts()['A']
        store_count = board.get_store_counts()[self.side]

        # TODO: if no seed can make it to the store, then what?

        # good: a pit has exactly the amount of seeds to make it
        # to the store in the next round
        perf_dist = 0
        # if board.perf_dist_from_store('A'):
        if board.perf_dist_from_store(self.side):
            perf_dist = 1

        # good: more seeds on own side of board
        # pit_count = board.get_player_seeds('A')
        pit_count = board.get_player_seeds(self.side)

        return 0.5 * store_count + 0.25 * perf_dist + 0.25 * pit_count
    
    def eval_func_research(self, board: Board):
        store_count = board.get_store_counts()[self.side]
        pit_count = board.get_player_seeds(self.side)
        # return 0.75 * store_count + 0.25 * pit_count
        return 0.5 * store_count + 0.5 * pit_count
    
    # From research paper
    # This modified minimaxing function returns the best action to take for the passed-in
    # player given a state (board layout)
    def modified_minimax(self, player, board: Board, alpha, beta, tree_level):
        # stopping conditions
        if not (self.at_terminal_state(board) or self.at_max_depth(tree_level)):
            # get action leading to extra turn, if any
            action = self.last_seed_to_kahala(player, board)

            # extra turn possible; take immediately
            if action:
                return action
            
            # get action leading to capture, if any
            action = self.last_seed_to_target_simple(player, board)

            # capture possible; take immediately
            if action:
                return action
            
            # none of the special cases above have been met; commence standard minimaxing
            return self.standard_minimax(player, board, alpha, beta, tree_level)["action"]

        # this shouldn't happen 
        return None
    
    # From research paper
    # Returns the first-discovered action leading to a capture for the passed-in player
    def last_seed_to_target_simple(self, player, board: Board):
        for action in board.get_legal_actions(player):
            board_copy = copy.deepcopy(board)
            board_copy.move_seeds(action, player)

            # get resulting capture, if any
            capture = board_copy.get_capture()

            # capture exists
            if capture:
                capturing_player, capturing_pit, captured_pit = capture

                # extra safety check
                if capturing_player == player:
                    return action

    # From research paper
    # Returns first-discovered action leading to an extra move for the passed-in player
    def last_seed_to_kahala(self, player, board: Board):
        for action in board.get_legal_actions(player):
            board_copy = copy.deepcopy(board)
            board_copy.move_seeds(action, player)

            # extra check to make sure it's the passed-in playe that gets the advantage
            if board_copy.gets_extra_move() == player:
                return action

    # From research paper
    # This minimaxing function returns a dictionary of the best action to take and its associated value 
    # According to the paper, the optimal depth is 4
    def standard_minimax(self, player, board: Board, alpha, beta, tree_level):
        # print(f'tree level:{tree_level}')
        if self.at_terminal_state(board) or self.at_max_depth(tree_level):
            return {"value": self.eval_func_research(board), "action": None}
        
        best_value = 0
        best_action = None

        # take maximizing pov
        if player == self.side:
            best_value = float('-inf')

            # print(f'Getting legal actions for {self.side}')
            for action in board.get_legal_actions(self.side):
                board_copy = copy.deepcopy(board)
                board_copy.move_seeds(action, self.side)

                # an extra turn is possible (last seed landed in own store)
                if board_copy.gets_extra_move() == self.side:
                    result = self.standard_minimax(self.side, board_copy, alpha, beta, tree_level)
                else:
                    result = self.standard_minimax(self.opponent_side, board_copy, alpha, beta, tree_level + 1)
                    
                if result["value"] > best_value:
                    best_value = result["value"]
                    best_action = action

                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
        else: # take opponent's (minimizing) pov 
            best_value = float('inf')

            for action in board.get_legal_actions(self.opponent_side):
                board_copy = copy.deepcopy(board)
                board_copy.move_seeds(action, self.opponent_side)

                # an extra turn is possible for agent's opponent (last seed landed in opponent's store)
                if board_copy.gets_extra_move() == self.opponent_side:
                    result = self.standard_minimax(self.opponent_side, board_copy, alpha, beta, tree_level)
                else:
                    result = self.standard_minimax(self.side, board_copy, alpha, beta, tree_level + 1)

                if result["value"] < best_value:    
                    best_value = result["value"]
                    best_action = action

                beta = min(beta, best_value)
                if beta >= alpha:
                    break
        
        return {"value": best_value, "action": best_action}

    
    def value(self, board: Board, tree_level, alpha, beta):
        if self.at_terminal_state(board) or self.at_max_depth(tree_level):
            return (self.eval_func(board), None)
        elif self.agent_is_min(tree_level):
            return self.min_value(board, tree_level, alpha, beta)
        else:
            return self.max_value(board, tree_level, alpha, beta)

    def max_value(self, board: Board, tree_level, alpha, beta):
        max_score = float('-inf')
        next_action = None

        # iterate through pits player can select
        for action in board.get_legal_actions(self.side):

            # consider a possible future without changing the original board
            board_copy = copy.deepcopy(board)
            board_copy.move_seeds(action, self.side)

            # get estimated utility of state after completing action
            val = self.value(board_copy, tree_level + 1, alpha, beta)[0]

            # value is greater than minimum value (beta)
            # return right away (the maximizer will prefer this node anyway)
            if val > beta:
                return (val, action)

            if val > max_score:
                max_score = val
                next_action = action

            # update best value seen by maximizers
            if max_score > alpha:
                alpha = max_score

        # return (utility, action) that leads to best (highest) estimated utility
        return (max_score, next_action)
    
    def min_value(self, board: Board, tree_level, alpha, beta):
        min_score = float('inf')
        next_action = None

        # iterate through pits player can select
        for action in board.get_legal_actions(self.opponent_side):

            # consider a possible future without changing the original board
            board_copy = copy.deepcopy(board)
            board_copy.move_seeds(action, self.opponent_side)

            # get estimated utility of state after completing action
            val = self.value(board_copy, tree_level + 1, alpha, beta)[0]

            # value is less than best value (alpha)
            # return right away (the minimizer will pick this node anyway)
            if val < alpha:
                return (val, action)

            if val < min_score:
                min_score = val
                next_action = action

            # update best value seen by minimizers
            if min_score < beta:
                beta = min_score

        # return (utility, action) that leads to best (lowest) estimated utility
        return (min_score, next_action)


    def at_terminal_state(self, board: Board):
        return board.at_terminal_state()
        # return False
    

    def agent_is_min(self, tree_level):
        # i.e, player is opponent
        return tree_level % 2 == 1
    

    def at_max_depth(self, tree_level):
        return tree_level / 2 == self.depth


class Game:
    def __init__(self):
        self.board = Board()
        self.next_player = 'B'

    def display_winner(self):
        scores = self.board.tally_up()
        b_score = scores['B']
        a_score = scores['A']

        print('Scores')
        print(f'B: {b_score}')
        print(f'A: {a_score}')

        if b_score < a_score:
            print('Red won!')
        elif b_score > a_score:
            print('Blue won!')
        else:
            print('Tie!')

    def run_agent_vs_agent(self):
        north_agent = Agent(4, 'A', 'B') # associated with A
        south_agent = Agent(4, 'B', 'A') # associated with B

        print("Place your bets... It's the computer against itself!")
        print("Starting board: ")
        self.print_mancala_board()
        print()

        while not self.at_terminal_state():
            if self.get_next_player() == 'B':
                tic = time.perf_counter()
                pit_choice = south_agent.get_next_action(self.board)
                toc = time.perf_counter()
                print(f"Decision took {toc - tic} seconds")

                # add 1 because 0-indexing is weird to read
                print(f"Blue chose pit # {pit_choice + 1}")

                self.move_seeds(int(pit_choice), 'B') 
            else:
                tic = time.perf_counter()
                pit_choice = north_agent.get_next_action(self.board)
                toc = time.perf_counter()
                print(f"Decision took {toc - tic} seconds")

                print(f"Red chose pit # {pit_choice}")
                self.move_seeds(int(pit_choice), 'A')

            self.print_mancala_board()
            print()
            self.display_capture()
            print()

        self.display_winner()

    def run_human_vs_agent(self):
        # create computer agent and set its cutoff depth
        computer = Agent(4, 'A', 'B')

        print("Welcome to Mancala! Here is the starting board. ")
        print("Computer: RED")
        print("You: BLUE")
        print("Player pits numbered from 1-6, left to right.")
        self.print_mancala_board()
        print()

        # TESTING
        # print(f"next player: {game.get_next_player()}")
        while not self.at_terminal_state():
            if self.get_next_player() == 'B':
                pit_choice = input("Please enter a pit number to distribute marbles from: ")

                if not (1 <= int(pit_choice) <= 6):
                    print("Invalid pit choice (select 1-6)")
                    continue

                print(f"You chose: pit # {pit_choice}")

                # subtract 1 from pit_choice to get correct index on board
                self.move_seeds(int(pit_choice) - 1, 'B') 
            else:
                tic = time.perf_counter()
                pit_choice = computer.get_next_action(self.board)
                toc = time.perf_counter()
                print(f"Decision took {toc - tic} seconds")
                print(f"Computer chose: pit # {pit_choice}")
                self.move_seeds(int(pit_choice), 'A')
            self.print_mancala_board()
            print()
            self.display_capture()
            print()

        self.display_winner()


    def print_mancala_board(self):
        self.board.print_board()
    

    def move_seeds(self, pit_num, player):
        self.board.move_seeds(pit_num, player)
        if player == 'B':
            self.next_player = 'A'
        else:
            self.next_player = 'B'
    

    def at_terminal_state(self):
        return self.board.at_terminal_state()


    def get_next_player(self):
        if not (self.board.gets_extra_move() == None):
            return self.board.gets_extra_move()
        return self.next_player
    
    
    def display_capture(self):
        capture_result = self.board.get_capture()

        # TESTING
        # print(f"capture_result: {capture_result}")
        
        if capture_result:
            capturing_player, capturing_pit, captured_pit = capture_result
            # account for zero-indexing for B's pits
            if capturing_player == 'A':
                captured_pit += 1 
            print(f"{capturing_player} has captured seeds from pit # {captured_pit}!") 
            self.board.perform_capture()
            self.print_mancala_board()
        return 


def main():
    game = Game()

    valid_option_picked = False
    game_choice = 6 # default option

    # query user for valid game option
    while not valid_option_picked:
        game_choice = input("Enter 6 to play against the computer OR 7 to see the computer play against itself: ")

        if not (int(game_choice) == 6 or int(game_choice) == 7):
            print("Please enter a valid option")
            continue

        valid_option_picked = True

    if int(game_choice) == 6:
        game.run_human_vs_agent()
    else:
        game.run_agent_vs_agent()

if __name__ == '__main__':
    main()