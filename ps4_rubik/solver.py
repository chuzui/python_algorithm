import rubik
class State:
    def __init__(self,position,parent,perm):
        self._position = position
        self._parent = parent
        self._perm = perm

    def __eq__(self, other):
        return self._position == other._position

def shortest_path(start, end):
    start_set = set()
    end_set = set()
    middle_set = set()

    start_set.add(State(start, None, None))
    end_set.add(State(end, None, None))

    filter_start_set = set()
    filter_end_set = set()
    filter_start_set.update(start_set)
    filter_end_set.update(end_set)

    while True:
        for state in start_set:
            for op in rubik.quarter_twists:
                new_state = State(rubik.perm_apply(op, state), state, op)
                if not new_state in filter_start_set:
                    middle_set.add(new_state)
        start_set = middle_set.copy()
        filter_start_set.update(middle_set)
        middle_set.clear()

        for state in end_set:
            for op in rubik.quarter_twists:
                new_state = State(rubik.perm_apply(op, state), state, op)
                if not new_state in filter_end_set:
                    middle_set.add(new_state)
        start_set = middle_set.copy()
        filter_end_set.update(middle_set)
        middle_set.clear()

        union_set = start_set.union(end_set)
        if len(union_set) > 0:
            for x in union_set:





