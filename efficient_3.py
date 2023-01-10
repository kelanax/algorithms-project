# Names: Aaishah Kelani, Ari Waller, Frances Watson
# USC ID: aaishahk, ariellew, fwatson
# CS 570 - Algorithms

import sys
import time
import os
#import tracemalloc
# from resource import *
#from streamlit import legacy_caching
import psutil

GAP_PENALTY = 30

DELTAS = {('A', 'A'): 0,
          ('A', 'C'): 110, 
          ('A', 'G'): 48,
          ('A', 'T'): 94, 
    }

MISMATCH_COST = {
    ('A', 'A'):0,
    ('A', 'C'): 110,
    ('A', 'G'): 48,
    ('A', 'T'): 94,
    ('C', 'C'):0,
    ('C', 'A'): 110,
    ('C', 'G'): 118,
    ('C', 'T'): 48,
    ('G', 'G'):0,
    ('G', 'A'): 48,
    ('G', 'C'): 118,
    ('G', 'T'): 110,
    ('T', 'T'):0,
    ('T', 'C'): 48,
    ('T', 'G'): 110,
    ('T', 'A'): 94,
    }

# Reads data from an input file. Generates two strings based on instructions
# from the input file. Outputs the two strings generated
#
# param   path           Name if the input file, default 'input.txt' is used
#                        if file is not specified
# return  str1, str2     Two strings generated per instructions in input file
def readInput(path="input.txt"):

    with open(path, 'r') as f:
        
        first, second = list(), list()
        locs_first, locs_second = [], [] 
        first_word_found, sec_word_found = False, False
        j, k = 0, 0

        for line in f:
            line = line.strip()
            int_check = isInt(line)
            
            if not int_check :
                if not first_word_found : 
                    first_word_found = True
                    first.append(line)
                else : 
                    sec_word_found = True
                    second.append(line)
            else :
                if not sec_word_found : 
                    locs_first.append(int(line))
                    j += 1
                else : 
                    locs_second.append(int(line))
                    k += 1
            
        first.append(locs_first)
        first.append(j)

        second.append(locs_second)
        second.append(k)

        str1, str2 = generate_str(first, second)
        are_strs_valid = validate_input(first[0], str1, j, second[0], str2, k)

        if are_strs_valid : return str1, str2
        else : return -1, -1

# Tests if the value passed in is an integer
#
# param   value     Value to be tested to determine if it is an integer
# return  boolean   Return True if value is an int, else return False
def isInt(value) :
    if value == '0' : return True
    return value.lstrip('-+').rstrip('0').rstrip('.').isdigit()        

def generate_str(first, second) :
    str1 = first[0]
    locs_first = first[1]
    j = first[2]
    
    str2 = second[0]
    locs_second = second[1]
    k = second[2]

    for loc in locs_first : 
        str1 = str1[:(loc+1)] + str1 + str1[(loc+1):]

    for loc in locs_second : 
        str2 = str2[:(loc+1)] + str2 + str2[(loc+1):]

    return str1, str2

# Checks whether the strings passed in are of the appropriate length 
# according to the length of each string before transposition
# 
# param   before_str_1        String 1 from input file before any changes
# param   str1                String 1 after string generation
# param   j                   The number of string 1 concatenations
# param   before_str_2        String 2 from input file before any changes
# param   str2                String 2 after string generation
# param   k                   The number of string 2 concatenations
# return                      Return True if both strings are of expected length
#                             or False otherwise
def validate_input(before_str_1, str1, j, before_str_2, str2, k) :
    len1 = len(before_str_1)
    exp_len1 = (2**j) * len1

    len2 = len(before_str_2)
    exp_len2 = (2**k * len2)

    actual_len1 = len(str1)
    actual_len2 = len(str2)

    if exp_len1 != actual_len1 : return False
    if exp_len2 != actual_len2 : return False

    return True

# Writes the results of an optimal alignment algorithm run to an output file
#
# param   cost      Cost of the optimal alignment
# param   x         Optimal alignment of string x
# param   y         Optimal alignment of string y
# param   time      Total time taken to complete run of the algorithm
# param   memory    Peak memory used in the duration of the algorithm
# param   path      Path specifying the location of the output file. Default
#                   path used is 'output.txt'
def write_output(cost, x, y, time, memory, path="output.txt") :
     with open(path, 'w') as f :
          f.write(str(cost) + '\n')
          f.write(x + '\n')
          f.write(y + '\n')
          f.write(str(time) + '\n')
          f.write(str(memory))


# Calculates the optimal cost of alignment between two strings as well as the optimal
# alignment. (Note: this algorithm is not memomory efficient)
#
# param   str1           One of the strings to be aligned
# param   str2           One of the strings to be aligned
# return  align_str1     The optimal alignment of the 1st string
# return  align_str2     The optimal alignment of the 2nd string
# return  cost           The optimal cost of the alignment between both strings
def basic_align(str1, str2) :
     opt =  {}
     for i in range(len(str1)+1):
          opt[i, 0] = i * GAP_PENALTY
     for j in range(len(str2)+1):
          opt[0, j] = j * GAP_PENALTY
     
     for i in range(1, len(str1) + 1) :
          for j in range(1, len(str2) + 1) :
               case_1 = opt[i-1, j-1] + MISMATCH_COST[str1[i-1],str2[j-1]]
               case_2 = opt[i-1, j] + GAP_PENALTY
               case_3 = opt[i,j-1] + GAP_PENALTY
               opt[i, j] = min(case_1, case_2, case_3)

     align_str1 = ""
     align_str2 = ""
     m, n = len(str1), len(str2)
     max_score = opt[m,n]

     while m> 0 and n>0 :
          score = opt[m,n]
          score_diag = opt[m-1,n-1]
          score_left = opt[m-1, n]
          score_down = opt[m, n-1]
          min_score = min(score_diag, score_left, score_down)

          if score == score_diag + MISMATCH_COST[str1[m-1],str2[n-1]] :
               align_str1 = str1[m-1] + align_str1
               align_str2 = str2[n-1] + align_str2
               m -= 1
               n -= 1
          elif score == score_left + GAP_PENALTY :
               align_str1 = str1[m-1] + align_str1
               align_str2 = '_' + align_str2
               m -= 1
          elif score == score_down + GAP_PENALTY :
               align_str1 = '_' + align_str1
               align_str2 = str2[n-1] + align_str2
               n -= 1
     while m > 0 :
          align_str1 = str1[m-1] + align_str1
          align_str2 = '_' + align_str2
          m -= 1
     while n > 0 : 
          align_str1 = '_' + align_str1
          align_str2 = str2[n-1] + align_str2
          n -= 1
     return align_str1, align_str2, max_score

# Returns the index of the minumum cost split point between aligning two strings
#
# param   opt_L          Dictionary containing the costs of aligning the left half 
#                        of string 1 with all of string 2
# param   opt_R          Dictionary containing the costs of aligning the right half
#                        of string 1 with all of string 2
# param   len_str2       Length of the second string
# return  min_i          Index of the minimum cost splitting point to align str1 to str2
def find_min_index(opt_L, opt_R, len_str2) :
     end = len_str2
     min_cost = 1000000000
     min_i = -1

     for i in range(len_str2 + 1) :
          cost = opt_L[i] + opt_R[end - i]
          if cost < min_cost : 
               min_cost, min_i = cost, i
     return min_i

# Memory efficient algorithm to calculate the optimal cost associated with aligning 
# string 1 to string 2
#
# param   str1      A string to be aligned
# param   str2      A string to be aligned
# return            Dictionary containing the last two columns of the costs to
#                   all of str1 to str2
def get_opt_align_column(str1, str2) :
     OPT = {}
     len_str1, len_str2 = len(str1), len(str2)
     for i in range(len_str2+1):
          OPT[0, i] = i * GAP_PENALTY
     curr_col = 1 # start in column 1 of the OPT array
     
     # ADD BASE CASES FOR IF EITHER STRING EQUALS 0

     # base cases
     for i in range(1, len_str1 + 1) :
          for j in range(len_str2 + 1) :
               if curr_col % 2 == 0 : curr_col, prev_col = 0, 1
               else : curr_col, prev_col = 1, 0
          
               if j == 0 : OPT[curr_col,j] = GAP_PENALTY * i
               else : 
                    # case 1 = str1 & str2 have a mismatch penalty --> continue with 
                    #                                                  str1[m-1] & str2[n-1]
                    # case 2 = str1 has a gap that matches position n of str2 --> str1[m-1], str2[n]
                    # case 3 = str2 has a gap that matches position n of str1 --> str1[m], str2[n-1]
                    
                    case_1 = OPT[prev_col, j-1] + MISMATCH_COST[str1[i-1],str2[j-1]]
                    case_2 = OPT[prev_col, j] + GAP_PENALTY
                    case_3 = OPT[curr_col,j-1] + GAP_PENALTY
                    OPT[curr_col, j] = min(case_1, case_2, case_3)
          curr_col += 1

     curr_col -= 1
     final_col = []
     for i in range(len_str2 + 1) : 
          final_col.append(OPT[curr_col, i])
     return final_col

# A divide and conquer recursive algorithm that calculates and determines the optimal 
# cost of alignment and the alignment between two strings.
#
# param   str1           A string to be aligned
# param   str2           A string to be aligned
# return  str1_result    The optimal alignment of the 1st string
# return  str2_result    The optimal alignment of the 2nd string
# return  final_cost     The optimal cost of the alignment between both strings           
def eff_sol(str1, str2) :
     str1_len, str2_len = len(str1), len(str2)

     if str1_len <= 2 or str2_len <= 2 :
          return basic_align(str1, str2)
     
     str1_L, str1_R = str1[:str1_len//2], str1[str1_len//2:]
                         
     # reverse the order of the str1_R and str2 to maintain consistency
     # in evaluating the optimal solution
     rev_str1_R, rev_str2 = str1_R[::-1], str2[::-1]

     opt_align_L, opt_align_R = get_opt_align_column(str1_L, str2), get_opt_align_column(rev_str1_R, rev_str2)
     min_index = find_min_index(opt_align_L, opt_align_R, str2_len)
     opt_align_L, opt_align_R = [], []

     x_L, y_L = str1[:(str1_len//2)], str2[:min_index]
     x_R, y_R = str1[(str1_len//2):], str2[min_index:]

     res_X_L, res_Y_L, cost_L = eff_sol(x_L, y_L)
     res_X_R, res_Y_R, cost_R = eff_sol(x_R, y_R)

     str1_result, str2_result, final_cost = res_X_L + res_X_R, res_Y_L + res_Y_R, cost_L + cost_R

     return str1_result, str2_result, final_cost

def process_memory() : 
     #process = psutil.Process(os.getpid())
     process = psutil.Process()
     mem = process.memory_info().rss
     return mem

def test() : 
     # remove hastags from the imports below to run
     #import  numpy as np
     #import pandas as pd
     #from streamlit import legacy_caching
     legacy_caching.clear_cache()
     output = []
     
     for i in range(1, 16) : 
          path = './datapoints/in{num}.txt'.format(num = i)
          start = time.time()

          str1, str2 = readInput(path)
          output_str1, output_str2, cost = eff_sol(str1, str2)

          end = time.time()
          total_time = (end - start)*1000

          memory_after = process_memory() 
          memory_consumed = int((memory_after)/1024)

          data = []
          data.append(i)
          data.append(len(str1) + len(str2))
          data.append(total_time)
          data.append(memory_consumed)

          output.append(data)
     array = np.array(output)
     pd.DataFrame(array).to_csv('graph_data_eff.csv', header=None, index=None)

#################################################################
######################## MAIN METHOD ############################

if __name__ == "__main__" :

     # Generate data for test points:
     #test()

     start = time.time()

     input_file = sys.argv[1]
     if len(sys.argv) > 2 : output_file = sys.argv[2]
     else : output_file="output.txt"

     str1, str2 = readInput(input_file)
     output_str1, output_str2, cost = eff_sol(str1, str2)

     end = time.time()
     total_time = (end - start)*1000

     memory_info = process_memory() 
     memory_consumed = int(memory_info/1024)
     
     write_output(cost, output_str1, output_str2, total_time, memory_consumed, output_file)
     
     #'''
