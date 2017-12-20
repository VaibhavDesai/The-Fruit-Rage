# The-Fruit-Rage
This is a software agent that can play this game against a human or another agent.

#Rules of the game

The Fruit Rage is a two player game in which each player tries to maximize his/her share from a batch of fruits randomly placed in a box. The box is divided into cells and each cell is either empty or filled with one fruit of a specific type.
At the beginning of each game, all cells are filled with fruits. Players play in turn and can pick a cell of the box in their own turn and claim all fruit of the same type, in all cells that are connected to the selected cell through horizontal and vertical paths. For each selection or move the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move. Once an agent picks the fruits from the cells, their empty place will be filled with other fruits on top of them (which fall down due to gravity), if any. In this game, no fruit is added during game play. Hence, players play until all fruits have been claimed.

10 x 10 game board with 4 types of fruits denoted by digits 0, 1, 2 and 3 in the cells. By analyzing the game, your agent should decide which location to pick next.

End of game: when the board is empty (no more fruits), the game is over. The score of each agent is the total points accumulated during the whole game (the sum of [fruits taken on each move]^2). The agent with the highest score wins. If both agents scored the same, the one with the most remaining time wins (to avoid draws during the competition).
