voting_data = list(open("voting_record_dump109.txt"))

## Task 1

def create_voting_dict():
    """
    Input: None (use voting_data above)
    Output: A dictionary that maps the last name of a senator
            to a list of numbers representing the senator's voting
            record.
    Example: 
        >>> create_voting_dict()['Clinton']
        [-1, 1, 1, 1, 0, 0, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1]

    This procedure should return a dictionary that maps the last name
    of a senator to a list of numbers representing that senator's
    voting record, using the list of strings from the dump file (strlist). You
    will need to use the built-in procedure int() to convert a string
    representation of an integer (e.g. '1') to the actual integer
    (e.g. 1).

    You can use the split() procedure to split each line of the
    strlist into a list; the first element of the list will be the senator's
    name, the second will be his/her party affiliation (R or D), the
    third will be his/her home state, and the remaining elements of
    the list will be that senator's voting record on a collection of bills.
    A "1" represents a 'yea' vote, a "-1" a 'nay', and a "0" an abstention.

    The lists for each senator should preserve the order listed in voting data. 
    """
    d = dict()
    for line in voting_data:
        l = line.split()
        d[l[0]] = list(map(int, l[3:]))
    return d
    

## Task 2

def policy_compare(sen_a, sen_b, voting_dict):
    """
    Input: last names of sen_a and sen_b, and a voting dictionary mapping senator
           names to lists representing their voting records.
    Output: the dot-product (as a number) representing the degree of similarity
            between two senators' voting policies
    Example:
        >>> voting_dict = {'Fox-Epstein':[-1,-1,-1,1],'Ravella':[1,1,1,1]}
        >>> policy_compare('Fox-Epstein','Ravella', voting_dict)
        -2
    """
    return sum([x*y for x,y in zip(voting_dict[sen_a], voting_dict[sen_b])])


## Task 3

def most_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is most
            like the input senator (excluding, of course, the input senator
            him/herself). Resolve ties arbitrarily.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> most_similar('Klein', vd)
        'Fox-Epstein'

    Note that you can (and are encouraged to) re-use you policy_compare procedure.
    """
    max_value = -len(voting_dict[sen])
    for name in voting_dict:
        if name != sen:
            value = policy_compare(sen, name, voting_dict)
            if value > max_value:
                max_value = value
                max_name = name
    return max_name
    

## Task 4

def least_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is least like the input
            senator.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> least_similar('Klein', vd)
        'Ravella'
    """
    min_value = len(voting_dict[sen])
    for name in voting_dict:
        if name != sen:
            value = policy_compare(sen, name, voting_dict)
            if value < min_value:
                min_value = value
                max_name = name
    return max_name
    
    

## Task 5

most_like_chafee = most_similar('Chafee' , create_voting_dict())
least_like_santorum = least_similar('Santorum', create_voting_dict())



democrats_set = set()
for line in voting_data:
    l = line.split()
    if l[1] == 'D':
        democrats_set.add(l[0])

# Task 6

def find_average_similarity(sen, sen_set, voting_dict):
    """
    Input: the name of a senator, a set of senator names, and a voting dictionary.
    Output: the average dot-product between sen and those in sen_set.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> find_average_similarity('Klein', {'Fox-Epstein','Ravella'}, vd)
        -0.5
    """
    n = len(sen_set)
    sum = 0
    for o_sen in sen_set:
        sum += policy_compare(sen, o_sen, voting_dict)
    return sum / n

most_average_Democrat = ... # give the last name (or code that computes the last name)


# Task 7

def find_average_record(sen_set, voting_dict):
    """
    Input: a set of last names, a voting dictionary
    Output: a vector containing the average components of the voting records
            of the senators in the input set
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> find_average_record({'Fox-Epstein','Ravella'}, voting_dict)
        [-0.5, -0.5, 0.0]
    """
    n = len(list(voting_dict.items())[0][1])
    m = len(sen_set)
    #print(n)
    v = [0 for i in range(n)]

    for sen in sen_set:
        v = [v[i] + voting_dict[sen][i] for i in range(n)]

    return [v[i] / m for i in range(n)]

average_Democrat_record = find_average_record(democrats_set, create_voting_dict()) # (give the vector)


# Task 8

def bitter_rivals(voting_dict):
    """
    Input: a dictionary mapping senator names to lists representing
           their voting records
    Output: a tuple containing the two senators who most strongly
            disagree with one another.
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> bitter_rivals(voting_dict)
        ('Fox-Epstein', 'Ravella')
    """
    voting_list = list(voting_dict)
    n = len(voting_list)
    min_value = 10000
    for i in range(n):
        for j in range(i+1, n):
            value = policy_compare(voting_list[i], voting_list[j], voting_dict)
            if value < min_value:
                min_value = value
                min_names = (voting_list[i], voting_list[j])
    return min_names

