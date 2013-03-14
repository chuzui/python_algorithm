import rubik

def positions_at_level(level):
    """
    Using BFS, returns the number of cube configurations that are
    exactly a given number of levels away from the starting position
    (rubik.I), using the rubik.quarter_twists move set.
    """
    if level == 0:
        return 1

    configurations_set = set()
    configurations_set.add(rubik.I)

    middle_set = set()
    filter_set = set()

    filter_set.update(configurations_set)
    for i in range(level - 1):
        for pos in configurations_set:
            for op in rubik.quarter_twists:
                middle_set.add(rubik.perm_apply(op, pos))
        configurations_set = middle_set.copy()
        filter_set.update(middle_set)
        middle_set.clear()


    for pos in configurations_set:
        for op in rubik.quarter_twists:
            new_state = rubik.perm_apply(op, pos)
            if not new_state in filter_set:
                middle_set.add(new_state)
    configurations_set = middle_set.copy()

    return len(configurations_set)

