import rubik

def count_repetitive_twists(moves):
    """
    When you apply the same twists to a cube over and over again, the
    cube will eventually return to its original position. This applies
    each move in moves repeatedly, until the cube returns to its
    original position, and counts the length of the cycle.
    """
    current_position = rubik.I
    for count in xrange(1, 100000):
        for move in moves:
            current_position = rubik.perm_apply(move, current_position)
        if(current_position == rubik.I):
            return count

if __name__ == "__main__":
    print count_repetitive_twists((rubik.F, rubik.L))  
