README.txt

Tommy Inouye
ti2181



Part 1)

Discuss the performance of your solver under various n parameters.

1) The lowest setting of n that lets your solver complete every puzzle in monday_puzzles with greater than 75% accuracy in terms of correct squares (before filling blank squares)
The lowest setting of n that lets my solver complete every puzzle in monday_puzzles. As shown below, the 
solver is able to complete all the puzzles but 1 with very good accuracy at n=1.

Here were the outputs when n=1:

 runtime_before_fill : 6.76
 total_squares : 189.00
 matching_squares_before_fill : 175.00
 runtime_before_fill : 7.62
 total_squares : 187.00
 matching_squares_before_fill : 166.00
 runtime_before_fill : 4.97
 total_squares : 187.00
 matching_squares_before_fill : 139.00
 runtime_before_fill : 5.95
 total_squares : 188.00
 matching_squares_before_fill : 179.00



2) The highest setting of n that lets my solver complete each of the puzzles in
monday_puzzles in less than 20 minutes is n=3. 

Here were the outputs when n=3:
 runtime_before_fill : 1332.08
 total_squares : 189.00
 matching_squares_before_fill : 175.00
 runtime_before_fill : 1420.40
 total_squares : 187.00
 matching_squares_before_fill : 174.00
 runtime_before_fill : 801.03
 total_squares : 187.00
 matching_squares_before_fill : 150.00
 runtime_before_fill : 1234.66
 total_squares : 188.00
 matching_squares_before_fill : 179.00



3) What does n represent?
N represents the branching factor at every node. Every node will have n children at most. 




To change n, all you have to do is change the corresponding paramater when it is being called in solve_puzzle.
I call solve_recursive(puz,variables,domains,weight_dict,neighbors,{},{},n,{}) so it is a matter of
changing that parameter




Part 2)







