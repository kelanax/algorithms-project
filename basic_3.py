# Names: Aaishah Kelani, Ari Waller, Frances Watson
# USC ID: aaishahk, ariellew, fwatson
# CS 570 - Algorithms

import sys
import time
#import tracemalloc
# from resource import *
import psutil
#from streamlit import legacy_caching


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

# This function will calculate the time calcluation for the basic algorithm.
def time_wrapper():
    start_time = time.time()
    call_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return time_taken

# This function will calculate the memory process for the basic algorithm.
def process_memory() : 
     #process = psutil.Process(os.getpid())
     process = psutil.Process()
     mem = process.memory_info().rss
     return mem



def optimalValue(sequence1, sequence2):

    # Create a dictionary to hold optimal values. 
    optimalValues = {}

    # Initialize values for optimal values dictionary. 
    for i in range(len(sequence2) + 1): 
        optimalValues[0, i] = i * GAP_PENALTY

    for i in range(len(sequence1) + 1):
        optimalValues[i, 0] = i * GAP_PENALTY

    for i in range(1,len(sequence1) + 1): 
        for j in range(1,len(sequence2) + 1): 
            case1 = optimalValues[i - 1, j - 1] + MISMATCH_COST[sequence1[i-1], sequence2[j-1]]
            case2 = optimalValues[i - 1, j] + GAP_PENALTY
            case3 = optimalValues[i, j - 1] + GAP_PENALTY
            optimalValues[i, j] = min(case1, case2, case3)
    return optimalValues

def optimalAlignment(sequence1, sequence2, optimalValuesDict):
    
    
    # Value of optimal solution is in the top right corner.
    # Trace back down the optimalValues dictionary from the top right corner. 
    
    i = len(sequence1)
    j = len(sequence2)

    optimalAlignmentSequence1 = ''
    optimalAlignmentSequence2 = ''
    
    while (i > 0 and j > 0): 
            optimalValueDiagonalCell = optimalValuesDict[i - 1, j - 1]
            optimalValueLeftCell = optimalValuesDict[i - 1, j]
            optimalValueBelowCell = optimalValuesDict[i, j - 1]
            optimalValueCurrentCell = optimalValuesDict[i, j]
            # Determine how we got to the current cell. 
            if (optimalValueCurrentCell == (optimalValueDiagonalCell + MISMATCH_COST[sequence1[i-1], sequence2[j-1]])):
                optimalAlignmentSequence1 = sequence1[i - 1] + optimalAlignmentSequence1
                optimalAlignmentSequence2 = sequence2[j - 1] + optimalAlignmentSequence2
                j = j - 1
                i = i - 1
            elif (optimalValueCurrentCell == (optimalValueLeftCell + GAP_PENALTY)):
                optimalAlignmentSequence1 = sequence1[i - 1] + optimalAlignmentSequence1
                optimalAlignmentSequence2 = '_' + optimalAlignmentSequence2
                i = i - 1
            elif (optimalValueCurrentCell == optimalValueBelowCell + GAP_PENALTY):
                optimalAlignmentSequence1 = '_' + optimalAlignmentSequence1
                optimalAlignmentSequence2 = sequence2[j - 1] + optimalAlignmentSequence2
                j = j - 1
    while (i > 0):
        optimalAlignmentSequence1 = sequence1[i - 1] + optimalAlignmentSequence1
        optimalAlignmentSequence2 = '_' + optimalAlignmentSequence2
        i = i - 1
    while (j > 0): 
        optimalAlignmentSequence1 = '_' + optimalAlignmentSequence1
        optimalAlignmentSequence2 = sequence2[j - 1] + optimalAlignmentSequence2
        j = j - 1
    return (optimalAlignmentSequence1, optimalAlignmentSequence2, optimalValuesDict[len(sequence1), len(sequence2)])

def test() : 
     #remove the hashtags from the imports below to run
     #import  numpy as np
     #import pandas as pd
     #from streamlit import legacy_caching
     legacy_caching.clear_cache()

     output = []
     
     for i in range(1, 16) : 
          path = './datapoints/in{num}.txt'.format(num = i)
          start = time.time()

          str1, str2 = readInput(path)
          optDict = optimalValue(str1, str2)
          output_str1, output_str2, cost = optimalAlignment(str1, str2, optDict)

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
     pd.DataFrame(array).to_csv('graph_data_basic.csv', header=None, index=None)

#################################################################
######################## MAIN METHOD ############################

if __name__ == "__main__" :



    input_file = sys.argv[1]
    str1, str2 = readInput(input_file)

    start = time.time()

    if len(sys.argv) > 2 : output_file = sys.argv[2]
    else : output_file="output.txt"
          
    optimalValueOfString1String2 = optimalValue(str1, str2)
    output_str1, output_str2, cost = optimalAlignment(str1, str2, optimalValueOfString1String2)
    cost = str(cost)
    end = time.time()
    total_time = (end - start)*1000
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    write_output(cost, output_str1, output_str2, total_time, memory_consumed, output_file)
