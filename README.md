## About
This project is a terminal-based mancala game. Users can select:
6) To play against a computer agent, or
7) To watch a computer agent play against itself

## Instructions
To run the game, ensure that python is installed on your computer (this project was written with python 3). Then, simply download game.py, navigate to the file on your terminal, and run python3 game.py. 

## How the Game Works
This game follows standard mancala rules. Each player selects a nonempty pit on their side of the board to distribute seeds from, in a counterclockwise fashion (the opponent’s store is skipped). If the last seed distributed lands in the player’s store, they are rewarded with an extra turn. Additionally, if the last seed lands in one of the player’s empty pits, opposite a nonempty opponent pit, the seeds from those two pits automatically go to the player’s store. This is called a capture. The game finishes when either side runs out of seeds in their pits. At this point, each player’s score is equal to the number of seeds in their store plus any remaining seeds in their pits.

When running the terminal game, the player (on the side of the blue pits) may select pits 1-6, provided that the selected pit is non-empty. 

## Technical Details
The computer agent makes decisions using the modified minimaxing algorithm in this paper: [Review of Kalah Game Research and the Proposition of a Novel Heuristic–Deterministic Algorithm Compared to Tree-Search Solutions and Human Decision-Making](https://www.researchgate.net/publication/344976321_Review_of_Kalah_Game_Research_and_the_Proposition_of_a_Novel_Heuristic-Deterministic_Algorithm_Compared_to_Tree-Search_Solutions_and_Human_Decision-Making).


## Graphics
Simple graphics borrowed from Neha Kennard: https://gist.github.com/nnkennard/ea8738f2bd9f8aff7d93837fc5c057f3