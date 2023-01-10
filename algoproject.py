#------------------------------------------#
# Title: <Enter Title here>.py
# Desc: <Enter Description here>
# Change Log: (Who, When, What)
# <Example Dev, 2030-Jan-01, Created File>
#------------------------------------------#



# -- DATA -- #



# -- PROCESSING -- #

def readInput(path="input.txt"):

    with open(path, 'r') as f:
        
        first = list()
        second = list()
        locs_first = []
        locs_second =[] 
        first_word_found = False
        sec_word_found = False
        j = 0
        k = 0

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



def isInt(value) :
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

def writeOutput(path="output.txt") :
    return 0

# -- PRESENTATION (Input/Output) -- #


GAP_PENALTY = 30

DELTAS = {('A', 'A'): 0,
          ('A', 'C'): 110, 
          ('A', 'G'): 48,
          ('A', 'T'): 94, 
    }


testSequence1 = ['G', 'C']
testSequence2 = ['C','C']


mismatchCost = {
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


optimalValues = {}
optimalValues[0,0] = 0
optimalValues[0, len(testSequence2)] = len(testSequence2) * GAP_PENALTY
optimalValues[len(testSequence1), 0] = len(testSequence1) * GAP_PENALTY

for i in range(len(testSequence2)+1):
    optimalValues[0, i] = i * GAP_PENALTY

for i in range(len(testSequence1)+1):
    optimalValues[i, 0] = i * GAP_PENALTY


def optimal(sequence1, sequence2):
    print(sequence1)
    print(sequence2)
    if len(sequence1) == 0:
        return optimalValues[0, len(sequence2)]
    if len(sequence2) == 0:
        return optimalValues[len(sequence1), 0]
    for key, value in enumerate(sequence1, start=1):
        for key2, value2 in enumerate(sequence2, start=1):
            print('key', key, value)
            print('key2', key2, value2)
            print()
            optimalValues[key, key2] = min(optimal(sequence1[key+1:], sequence2[key2+1:])+mismatchCost[value, value2], optimal(sequence1[key+1:], sequence2) + GAP_PENALTY, optimal(sequence1, sequence2[key2+1:]) + GAP_PENALTY)
            #if (key, key2) not in optimalValues:
                #optimalValues[key, key2] = min(optimal(sequence1[key+1:], sequence2[key2+1:])+mismatchCost[value, value2], optimal(sequence1[key+1:], sequence2) + GAP_PENALTY, optimal(sequence1, sequence2[key2+1:]) + GAP_PENALTY)
                #print('optimal value in fn if', optimalValues[key, key2])
            #else:
                #print('optimal value in fn', optimalValues[key, key2])
                #return optimalValues[key, key2]
    return optimalValues[len(sequence1), len(sequence2)]


'''

def tester2(sequence1, sequence2): 
    for key1, value1 in enumerate(sequence1, start=1): 
        for key2, value2 in enumerate(sequence2, start=1):
            print('key1', key1, 'value1', value1)
            print('key2', key2, 'value2', value2)
            if (key1, key2) not in optimalValues:
                print('mismatch', mismatchCost[value1, value2])
                optimalValues[key1, key2] = min(optimal(sequence1[key1:], sequence2[key:])+mismatchCost[value, value2], optimal(sequence1[key:], sequence2) + GAP_PENALTY, optimal(sequence1, sequence2[key:]) + GAP_PENALTY)
            else:
                return optimalValues[key, key2]
    return optimalValues[len(sequence1), len(sequence2)]

'''

#tester2(testSequence1, testSequence2)


print('optimal final', optimal(testSequence1, testSequence2))


for key, value in optimalValues.items():
    print('key', key, 'value', value)

                
                
                
                
# -- MAIN METHOD -- #
                
                
                
                
                
