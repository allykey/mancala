import termcolor
from termcolor import colored, cprint
import random
import copy

# == Mancala ==================================================================

class Board:
    player_to_background = {"A": "on_red", "B": "on_blue"}

    def __init__(self):
        # start with B (user), then A (computer)
        # stores initially have 0 seeds
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    # get the seed count in a single specified pit
    def get_pit_seeds(self, pit_num):
        # if not (1 <= pit_num <= 6) or not (7 <= pit_num <= 12):
        if not (0 <= pit_num <= 5) and not (7 <= pit_num <= 12):
            return -1
        
        # # user (B)'s pit_num must subtract 1 to match indexing
        # if (1 <= pit_num <= 6):
        #     return self.board[pit_num - 1]
        
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

        # # subtract 1 to get correct index in board for user
        # if player == 'B':
        #     i -= 1

        # get number of seeds in pit
        num_seeds = self.board[i]

        # empty specified pit
        self.board[i] = 0

        # distribute seeds counter-clockwise
        while num_seeds > 0:
            i = (i + 1) % len(self.board)

            # skip opponent's store (home)
            if player == 'B' and i == len(self.board) - 1:
                continue
            elif player == 'A' and i == 6:
                continue

            self.board[i] += 1
            num_seeds -= 1

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

        return userDone or computerDone
    

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
    def __init__(self, depth):
        # cutoff depth for minimaxing
        self.depth = depth
        
    def get_next_action(self, board: Board):
        # must be pits 7-13
        next_action = 0 
        max_score = float('-inf')

        # consider all available pits
        for i in range(7, 13):
            # skip empty pits
            if board.get_pit_seeds(i) == 0:
                # TESTING
                print(f"pit {i} has no seeds, skip")
                continue

            board_copy = copy.deepcopy(board)
            board_copy.move_seeds(i, 'A')

            # TESTING
            # print("TESTING AGENT")
            # board_copy.print_board()

            val = self.value(board_copy)

            # TESTING
            # print(f"val: {val}")

            if val > max_score:
                max_score = val
                next_action = i

        return next_action

    # heuristic for getting utility of state
    def eval_func(self, board: Board):
        # TESTING
        # print(f"{board.get_store_counts()['A']}")

        # good: put seed in store
        utility = board.get_store_counts()['A']

        # TODO: if no seed can make it to the pit, then what?

        # good: a pit has exactly the amount of seeds to make it
        # to the store in the next round
        if board.perf_dist_from_store('A'):
            utility += 1

        return utility
    
    def value(self, board: Board):
        if self.at_terminal_state(board):
            return board.get_player_seeds('A') + board.get_store_counts()['A']
        else:
            return self.eval_func(board)
    
    def max_value(self, board: Board, treeLevel):
        return 0
    
    def min_value(self, board: Board, treeLevel):
        return 0
    
    def at_terminal_state(self, board: Board):
        # return board.at_terminal_state()
        return False
    
    def agentIsMin(self, player):
        return player == 'B'
    
    def atMaxDepth(self, treeLevel):
        return treeLevel / 2 == self.depth


class Game:
    # TODO: remove mancala_board (for testing only)
    mancala_board = {
        "A": [0, 4, 4, 4, 4, 4, 4], # computer's 
        "B": [0, 4, 4, 4, 4, 4, 4], # user's
        # "A": ['h:0', '1:4', '2:4', '3:4', '4:4', '5:4', '6:4'],
        # "B": ['h:0', '1:4', '2:4', '3:4', '4:4', '5:4', '6:4'],
    }

    def __init__(self):
        self.board = Board()
        self.next_player = 'B'

    def run(self):
        # create computer agent and set its cutoff depth
        computer = Agent(5)

        print("Welcome to Mancala! Here is the starting board. ")
        print("Computer: RED")
        print("You: BLUE")
        print("Player pits numbered from 1-6, left to right.")
        self.print_mancala_board()

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
                pit_choice = computer.get_next_action(self.board)
                print(f"Computer chose: pit # {pit_choice}")
                self.move_seeds(int(pit_choice), 'A')
            self.print_mancala_board()


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
        return self.next_player


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()