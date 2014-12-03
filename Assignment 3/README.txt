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
n represents the branching factor at every node. Every node will have n children at most. 


4) To change n, all you have to do is change the corresponding paramater when it is being called in solve_puzzle.
I call solve_recursive(puz,variables,domains,weight_dict,neighbors,{},{},n,{}) so it is a matter of
changing that parameter

Part 2)

Here was the results when n=1 
 matching_squares_after_fill : 176.00
 total_squares : 189.00
 matching_squares_after_fill : 169.00
 total_squares : 187.00
 matching_squares_after_fill : 140.00
 total_squares : 187.00
 matching_squares_after_fill : 180.00
 total_squares : 188.00


Explanation: For part 2, I decided to treat the problem as a CSP and try to implement a procedure
similar to the one used in part 1. I was successfully able to implement an algorithm that first figured out all the
possible words that can be filled in and then the combination of words that filled up as many squares as possible. 
I first read the answers_cwg_otsys.txt file and stored all the words into a dictionary where the key is the length of the word.
Then I started my algorithm that first found all the clues that can be filled in along with the word that fills it. 
Then I found the word with the highest domain and and filled it into the puzzle and recursively called the function with the updated puzzle.
The evaluation function was modified to count the number of spaces filled.  

Part 3)

How to test components:
I updated the components and ran the Monday puzzles with the new components and found that the performance improved for most of them. The assigned component is unfortunately triggered for every clue because there is no way to determine if a clue is asking for a definition or not. The original component is triggered whenever it is a fill in the blank style question and tries to see if a given clue is a book title.

To see each component in action, run these commands:
1) python definition_component.py < definition_test
2) python book_component.py < book_component

Assigned component: I was assigned component 24 which was dictionary definitions. This proved to be very tricky because no clues outright asks for a definition but rather gives a definition. 
I found that the wikipedia query did a very good job of returning the word from a dictionary definition with good confidence. But for obscure definitions or references, it was helpful to have an additional feature. Thus, I utilized a dictionary API http://developer.wordnik.com/ that allowed me to query for dictionary definitions of words. I then parsed the input and found the definition of the words in the definition and surprisingly enough, the original word comes up very frequently. So I combined the results of both by parsing the results that I receive and calculating the probability using word frequency. The more repeated a word is in both the wikipedia query and wordnik query, the higher it's probability. 
Assigned component performance: Unfortunately this component was not that great in improving the performance of the crossword puzzle solver. There is just no way to find out if the clue is asking for the definition of the clue and thus it is important for me to keep the resulting probabilities low because sometimes they are not remotely close to the answer but happen to be in the output. In almost all cases though, the word is always returned in the case that the definition was given but many of the times it is of very low probability or average. 

Here are some things to note about the wordnik API.
Link: http://developer.wordnik.com/
API Key: 0447438b71e16b1fe640c0524220f075951133d14bb14890e

I created an array of words to ignore because they are either too common or words that will never appear in a crossword. These words are ignored on the frequency count and are never returned as a possible word. I got the words from this link https://kb.iu.edu/d/afhf



Original component: My original component was to match clues for famous book titles. I had originally planned to create an array of common book titles and match them, but I found that almost any well-known book is easily found using the wikipedia query. Thus, I just stripped the "___" part of the clue and searched the clue in the wikipedia query. For every word in the output, I tested to see if there was an exact match in the clue and output and determined whether the word that was missing was the exact length of what we were looking for. 
Original Component performance: My original component was fortunately much better than the assigned component. Because it is very easy to figure out whether or not the input is a a fragment of a book title (I look to see if it is a fill in the blank), I can perform at a much higher confidence. I almost always find the right answer and I even sometimes find non book related fill in the blanks such as movie titles and famous phrases. 

