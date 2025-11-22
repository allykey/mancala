import termcolor
from termcolor import colored, cprint

# == Mancala ==================================================================

class Game:
    # TODO: remove - for testing purposes only
    count = 0

    mancala_board = {
        "A": [0, 4, 4, 4, 4, 4, 4], # computer's 
        "B": [0, 4, 4, 4, 4, 4, 4], # user's
        # "A": ['h:0', '1:4', '2:4', '3:4', '4:4', '5:4', '6:4'],
        # "B": ['h:0', '1:4', '2:4', '3:4', '4:4', '5:4', '6:4'],
    }

    # start with B (user), then A (computer)
    board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    player_to_background = {"A": "on_red", "B": "on_blue"}

    def move_seeds(self, pit_num, player):
        i = pit_num - 1
        num_seeds = self.board[i]
        self.board[i] = 0

        while num_seeds > 0:
            i = (i + 1) % len(self.board)

            # skip opponent's store (home)
            if player == 'B' and i == len(self.board) - 1:
                continue

            self.board[i] += 1
            num_seeds -= 1

        # i = pit_num + 1
        # num_seeds = self.mancala_board[player][pit_num]
        # i = pit_num + 1

        # # update player's board first (counterclockwise)
        # self.mancala_board[player][pit_num] = 0
        # while i < len(self.mancala_board[player]) and num_seeds > 0:
        #     self.mancala_board[player][i] += 1
        #     i += 1 
        #     num_seeds -= 1

        return

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


    def print_mancala_board(self):
        # self.print_home(self.mancala_board['A'][0], 'A')
        # for pit in self.mancala_board['A'][1:]:
        #     self.print_pit(pit, 'A')
        # self.print_home(self.mancala_board['B'][0], 'B')
        # print()
        # self.print_empty_home('A')
        # for pit in (self.mancala_board['B'][1:]):
        #     self.print_pit(pit, 'B')
        # self.print_empty_home('B')
        # print()    

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

    def atTerminalState(self):
        return False



def main():
    game = Game()
    print("Welcome to Mancala! Here is the starting board. ")
    print("Computer: RED")
    print("You: BLUE")
    print("Player pits numbered from 1-6, left to right.")
    game.print_mancala_board()

    while game.count < 10 and not game.atTerminalState():
        pit_choice = input("Please enter a pit number to distribute marbles from: ")
        print(f"You chose: pit # {pit_choice}")
        game.move_seeds(int(pit_choice), 'B')
        game.print_mancala_board()
        # print()
        game.count += 1

if __name__ == '__main__':
    main()