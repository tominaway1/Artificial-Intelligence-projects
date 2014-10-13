Heuristics:

	I have implemented two major strategies into my code that heavily impacted its performance. 
The first strategy is something that I researched on the internet (at this link http://www.samsoft.org.uk/reversi/strategy.html). It is called the evaporation strategy and it aims to minimize the number of pieces on the board in the beginning phases of the game. This helps to increase my relative mobility and 
and it is advantageous to me because I believe that most of my peers will not expect me to minimize my pieces making my AI more unpredictable. I do this for the first few moves. I also have implemented a positional strategy adding value to certain values of the board. This is 
taken into account in the calculation of my heuristic value in addition to the difference of pieces of the 
board. Of course, this is only after the first few turns that I implement the evaporation strategy. 
	However, the key implementation of my AI is how I handle edges. In my simulations of the game, I
realized I always aim to dominate the edges. This strategy gives me a huge advantage over the end game. 
The only danger is that it makes the corners a very important part of my game. I am very cautious about
leaving the corner squares vulnerable and actually made it so it is always the last option. This method
however heavily increased the efficiency of the program. Before min-max, I always run a check to see if 
there are any pieces on the edges of the board that will not be vulnerable the next turn. If there are, I
run a min-max on all those moves. Otherwise, I would run min-max on all the moves that are not adjacent
to the corner square. This effectively cuts down the number of nodes in my tree in half. It makes it so 
I have no trouble with a recursion depth of 4 and only runs min max on moves that are important.


