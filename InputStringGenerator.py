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

        if are_strs_valid : return first, second
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
        str1 = str1[:loc] + str1 + str1[loc:]

    for loc in locs_second : 
        str2 = str2[:loc] + str2 + str2[loc:]

    return str1, str2


def validate_input(before_str_1, str1, j, before_str_2, str2, k) :
    len1 = len(before_str_1)
    exp_len1 = (2**j) * len1

    len2 = len(before_str_2)
    exp_len2 = (2**k * len2

    actual_len1 = len(str1)
    actual_len2 = len(str2)

    if exp_len1 != actual_len1 : return False
    if exp_len2 != actual_len2 : return False

    return True



'''
# Test In Main Below:
                
if __name__ == "__main__" :

    str1, str2 = readInput(path="input1.txt")
'''

