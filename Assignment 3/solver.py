#! /usr/bin/python

## @package solver.py
# Solves a puzzle using components to generate candidates
#
# Steve Wilson
# Edited: Rui Zhang
# Apr 2014
# July 2014

import sys
import re
import argparse
import string
import subprocess
import random
import time
import csp.csp as csp
import puzzle
import copy
from component_thread import myThread

# @param puz the puzzle object
# @param candidates_file input file of candidate answers
# @param limit only take the top <limit> answers
def generate_all_candidates(puz,limit,score_adjust,candidates_output=None):
    print 
    print "======================== Merge All candidats answers ================"
    data = []
    if candidates_output:
        data = candidates_output.split('\n')
    else:
        data = sys.stdin()
    answers_given = {}
    for line in data:
        print "line", line
        if line == "":
            continue
        clue_id = None
        answer = None
        component_source = None
        score = 1
        try:
            items = line.split('\t')
            assert len(items) in [2,3,4]
        except:
#            raise IOError("format not recognized for line: "+line)
            continue
        else:
            if len(items) >= 2:
                clue_id,answer = items[:2]
            if len(items) >= 3:
                score = float(items[2])
            if len(items) == 4:
                component_source = items[3]
                score += score_adjust
            else:
                print "==========================abnormal length====================="	

        # make sure answer given is correct length
        assert len(answer) == puz.entries[clue_id].length

        if clue_id not in answers_given:
            answers_given[clue_id] = []
        skip = False
        for i in range(len(answers_given[clue_id])):
            if answer.upper() == answers_given[clue_id][i][0]:
                answers_given[clue_id][i]=(answer.upper(),float(score)+answers_given[clue_id][i][1],answers_given[clue_id][i][2]+[component_source])
                skip=True
        if not skip:
            answers_given[clue_id].append((answer.upper(),float(score),[component_source]))


    candidates = {}
    unanswered_clues = []
    for k in puz.entries.keys():
        if k in answers_given:
            candidates[k] = [x[0] for x in sorted(answers_given[k],key=lambda x:x[1], reverse=True)[:limit]]
        else:
	    #give unanswered_clue candidates as "-----"
            unanswered_clues.append(k)
            candidates[k] = []
            candidates[k].append('-'*puz.entries[k].length)

    puz.all_candidates = answers_given
    weights_dict = {}

    for k,answers in answers_given.items():
        weights_dict[k] = {}
        for answer in answers:
            weights_dict[k][answer[0]]=answer[1]

      
    #return candidates,weights_dict,unanswered_clues
    ''' evaluate merger results "candidates" '''
    rank_of_candidates = {}
    cnt = 0
    rank_sum = 0
    for k in candidates.keys():
	if candidates[k][0] != '-':
	    correct_answer = puz.entries[k].answer
            rank = 0
            find = False 

	    for candidate in candidates[k]:
                rank = rank + 1
                if candidate == correct_answer.upper():
                    rank_of_candidates[k] = rank
                    find = True
                    cnt = cnt + 1
                    rank_sum = rank_sum + rank
                    break

	    if find == False:
                rank_of_candidates[k] = -1
        else:
	    rank_of_candidates[k] = -1
    if cnt == 0:
        cnt = 1
    
    cnt_2 = 0
    temp_S = {}
    rank_answers = {}
    for k in puz.entries.keys():
        temp_S[k] = '-'*puz.entries[k].length
        rank_answers[k] = -1
    
    for k in answers_given.keys():
	rank = 0
        correct_answer = puz.entries[k].answer
        for candidate_tuple in sorted(answers_given[k],key=lambda x:x[1],reverse=True):
	    rank += 1
            if correct_answer.upper() == candidate_tuple[0]:
                temp_S[k] = correct_answer
		rank_answers[k] = rank
	        cnt_2 = cnt_2 + 1
                break

    ''' print how many candidates answers are generated for each clue'''
    tup_list = []
    for k in sorted(puz.entries.keys()):
        if k in answers_given.keys():
            if len(candidates[k])>1:
                first_score = weights_dict[k][candidates[k][0]]
                second_score = weights_dict[k][candidates[k][1]]
            else:
                first_score = weights_dict[k][candidates[k][0]]
		second_score = 0
	    tup_list.append((k,rank_answers[k],len(answers_given[k]),first_score,first_score-second_score))

        else:
	    tup_list.append((k,rank_answers[k],0,0,0))
    for tup in sorted(tup_list,key=lambda x:x[3],reverse=True):
        #print tup[0]+'\t'+str(tup[1])+' \ '+ str(tup[2])+'\t\t'+str(tup[3])+'\t'+str(tup[4])
        print tup[0]+'\t'+str(tup[1])+' \ '+ str(tup[2])

    print "max"+"\t"+str(max([rank_answers[k] for k in rank_answers.keys()]))+'/'+str(max([len(answers_given[k]) for k in answers_given.keys()])) 

    cnt_3 = 0
    for k in temp_S.keys():
        temp_S = puz.update_solution(temp_S,k)
    for k in temp_S.keys():
        if temp_S[k].upper() == puz.entries[k].answer.upper():
            cnt_3 += 1
    
    print 
    print "number of clues: " , len(puz.entries.keys())
    print "number of clues answered by some component: " , len(answers_given.keys())
    print "number of clues answered correctly by some component: " , cnt_2, "(",cnt_3,")"
    print "number of clues answered correctly in candidates list of CSP: " , cnt 
    print "with average rank: " , float(rank_sum)/cnt  , "/" , limit
    print 

    return candidates,weights_dict,unanswered_clues


class RebusError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def propagate(next_var, next_val, puz, domains, neighbors, S):
    print 'calling propagate ...........'

    # Check for assigned neighbors of next variable
    for neighbor in neighbors[next_var]:
        # if this neighbor is already assigned
        if neighbor in S.keys():
            if puz.check_intersect(neighbor,S[neighbor],next_var,next_val) == False:
                return False, None, None

    # Give assignment to next variable
    next_S = copy.deepcopy(S)
    next_S[next_var] = next_val
    next_S = puz.update_solution(next_S,next_var)

    # Pop next variable in next_domains
    next_domains = copy.deepcopy(domains)
    next_domains.pop(next_var)
    
    # Check for non-assigned neighbors of next variable
    for neighbor in neighbors[next_var]:
        if neighbor not in S.keys():
            for neighbor_candidate in domains[neighbor]:
                # if conflict, remove it
                if puz.check_intersect(neighbor,neighbor_candidate,next_var,next_val) == False:
                    next_domains[neighbor].remove(neighbor_candidate)

    return True, next_domains, next_S

def find_score(weight_dict,S):
    ans = 0

    for key in S:
        if key not in weight_dict:
            continue
        if S[key] in weight_dict[key]:
            ans += weight_dict[key][S[key]]
    return ans

def dict_length(P):
    ans = 0
    for key in P:
        ans += len(P[key])
    return ans


def solve_recursive(puz,variables,domains,weight_dict,neighbors,S_o,B_o,n,P_o):
    #base case
    if len(variables) == len(S_o.keys()):
        #return B or S depending which has higher score
        if find_score(weight_dict,S_o) > find_score(weight_dict,B_o):
            return S_o
        else:
            return B_o
    #recursive case
    S = copy.deepcopy(S_o)
    B = copy.deepcopy(B_o)
    P = copy.deepcopy(P_o)
    #find variable with maximum difference and find d
    max_diff = float("-inf")
    v = None
    d = None
    for var in variables:
        #check if already evaluated
        if var in S:
            continue
        #array of words already tried
        p_for_var = None
        if var in P:
            p_for_var = P[var]
        else:
            p_for_var = []

        #find difference from 1st and 2nd value not in P
        if var in domains:
            val_arr = domains[var]
        else: 
            val_arr = []

        if len(val_arr) == 0:
            S[var]= "-" * puz.entries[var].length
            for k in S.keys():
                S = puz.update_solution(S,k) 
            continue

        first = None
        second = None
        for i in val_arr:
            if i in p_for_var:
                continue
            if not first:
                first = i
                continue
            if not second:
                second = i
                continue
            break
        if (not first) or (not second):
            if second:
                S[var] = first
            else:
                S[var]= "-" * puz.entries[var].length
            for k in S.keys():
                S = puz.update_solution(S,k) 
            continue

        else:
            diff = weight_dict[var][first] - weight_dict[var][second]
            if diff > max_diff:
                max_diff = diff
                v = var
                d = first

    if len(variables) == len(S.keys()):
        #return B or S depending which has higher score
        if find_score(weight_dict,S) > find_score(weight_dict,B):
            return S
        else:
            return B
    # print len(variables)
    # print len(S.keys())
    success, next_domains, next_S = propagate(v,d,puz,domains,neighbors,S)

    if success:
        B = solve_recursive(puz,variables,next_domains,weight_dict,neighbors,next_S,B,n,P)
    
    if dict_length(P) < n:
        if v in P:
            temp = P[v]
            temp.append(d)
            P[v] = temp   
        else:
            P[v] = [d]
        temp = solve_recursive(puz,variables,domains,weight_dict,neighbors,S_o,B,n,P) 
        if find_score(weight_dict,temp) > find_score(weight_dict,B):
            return temp 
    return B



## Find a solution to the puzzle
def solve_puzzle(puz,component_output,mode,limit,score_adjust,second_round=True):
    if puz.is_rebus:
        raise RebusError("Solver cannot handle rebus style puzzles")

    puz.update_all_intersections()
    domains,weight_dict,unanswered_clues = generate_all_candidates(puz,limit,score_adjust,component_output)
 
    # construct CSP problem
    problem = csp.CSP(puz.entries.keys(),
                      domains,
                      {k:puz.entries[k].intersections.keys() for k in puz.entries.keys()},
                      puz.check_intersect)
    variables = puz.entries.keys()
    neighbors = {k:puz.entries[k].intersections.keys() for k in puz.entries.keys()}
    S = {}

    # assign variables which cannot be answered
    for k in unanswered_clues:
       	S[k] = domains[k][0] # this will be "-"*
        domains.pop(k)

    print "\nSolving CSP probelm ....."
    start = time.time()
    #solution = solve_recursive(puz,variables,domains,neighbors,S)
    solution = solve_recursive(puz,variables,domains,weight_dict,neighbors,{},{},1,{})
    end = time.time()
    print("\nCSP solver runtime: " + str(end-start))

    # evaluate solution
    print "\nEvaluating solution ...."
    evaluation = puz.evaluate_solution(problem,solution,'_before_fill')
    evaluation['runtime_before_fill'] = end-start

    # PART 2 GOES HERE - FILL IN BLANK SQUARES
    print "\nEvaluating filled solution ...."
    solution = fill(solution,weight_dict,puz)
    evaluation = puz.evaluate_solution(problem,solution,'_after_fill')

    end2 = time.time()
    print("\nBlank square filling runtime: " + str(end2-start))
    evaluation['runtime']=end2-start

    return evaluation,solution

def fill(solution,wd,puz):
    print solution
    f = open("../answers_cwg_otsys.txt")
    d = make_dict(f.read())
    ans = eval_sol(solution,wd,puz,d)
    print ans
    return ans

def eval_sol(solution,wd,puz,d):
    for key in solution:
        #get list of possible words
        temp = solution[key]
        arr = d[len(temp)]
        #see if any words match. Pick the one with highest domain
        max_word = None
        max_val = float("-inf")
        boolean = True
        if "-" not in temp:
            continue

        for item in arr:
            if key not in wd:
                continue
            if item not in wd[key]:
                continue
            if wd[key][item] > max_val:
                if check_letters(temp,item):
                    print key
                    max_val = wd[key][item]
                    max_word = item
        if max_word:
            solution[key] = max_word
            for k in solution.keys():
                solution = puz.update_solution(solution,k)
            print max_word
            print key
            return eval_sol(solution,wd,puz,d) 
    return solution

def check_letters(temp,item):
    length = len(temp)
    for i in range(length):
        if temp[i] != "-" and temp[i] != item[i]:
            print "-------"
            print temp[i]
            print item[i]
            print "-------"
            return False
    return True


def make_dict(bank):
    ans = {}
    arr = bank.split()
    for item in arr:
        key = len(item)
        if key not in ans:
            ans[key] = []
        ans[key].append(item)
    return ans

## Handle command line arguments
def arg_parse():
    parser = argparse.ArgumentParser(description="Import a .puz file as a python puzzle obect and output a solution.")
    parser.add_argument('puz_file', metavar='puz_file', type=str,
                        help='path to the .puz file to load')
    parser.add_argument('candidates_file', metavar='candidates_file', type=str,
                        help='path to component output to use when generating candidate answers')
    return parser.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    p = puzzle.Puzzle(args.puz_file)
    evaluation = solve_puzzle(p,open(args.candidates_file).read())
    print p.get_side_by_side_comparison()
    for k,v in sorted(evaluation.items()):
        print k+':'+'\t'+str(v)
