import math
def detect_collisions(balls):
    """
    Detect any pairs of balls that are colliding.
    Returns a set of ball_pairs.
    """
    n_balls = len(balls)
    world_min_x = -200.0*n_balls**.5  # minimum x in world coordinates
    world_max_x = +200.0*n_balls**.5  # maximum x in world coordinates
    world_min_y = -200.0*n_balls**.5  # minimum y in world coordinates
    world_max_y = +200.0*n_balls**.5  # maximum y in world coordinates
    set_of_collisions = set()

    set_of_collisions_2 = set()

#    for i in range(len(balls)):
#        b1 = balls[i]
#        for j in range(i):
#            b2 = balls[j]
#            if gas.colliding(b1, b2):
#                set_of_collisions_2.add(gas.ball_pair(b1, b2))

    cloumn_num = int(math.ceil(400 * n_balls**.5 / 256))
    squared_list = [[] for x in range(cloumn_num) for y in range(cloumn_num)]
    total_num = cloumn_num * cloumn_num
    for i in range(n_balls):
        x_pos = int(math.floor((balls[i].x - world_min_x) / 256))
        y_pos = int(math.floor((balls[i].y - world_min_y) / 256))
        squared_list[x_pos * cloumn_num + y_pos].append(balls[i])

    for i in range(len(squared_list)):
        for j in range(len(squared_list[i])):
            b1 = squared_list[i][j]
            for k in range(j):
                b2 = squared_list[i][k]
                if gas.colliding(b1, b2):
                    set_of_collisions.add(gas.ball_pair(b1, b2))
        # if(i >= cloumn_num):
        #     list_collisions(squared_list[i], squared_list[i - cloumn_num],set_of_collisions)
        if(i < total_num - cloumn_num):
            list_collisions(squared_list[i], squared_list[i + cloumn_num],set_of_collisions)
        # if i % cloumn_num > 0:
        #     list_collisions(squared_list[i], squared_list[i - 1],set_of_collisions)
        if i % cloumn_num < cloumn_num - 1:
            list_collisions(squared_list[i], squared_list[i + 1],set_of_collisions)

        if i < total_num - cloumn_num and  i % cloumn_num > 0:
            list_collisions(squared_list[i], squared_list[i + cloumn_num - 1],set_of_collisions)

        if i < total_num - cloumn_num and i % cloumn_num < cloumn_num - 1:
            list_collisions(squared_list[i], squared_list[i + cloumn_num + 1],set_of_collisions)


        #print "set_of_collisions_2 ", len(set_of_collisions_2)
        #print "set_of_collisions ", len(set_of_collisions)
    return set_of_collisions

def list_collisions(l1, l2, set_of_collisions):
    for b1 in l1:
        for b2 in l2:
            if gas.colliding(b1, b2):
                set_of_collisions.add(gas.ball_pair(b1, b2))



# def detect_collisions(balls):
#     """
#     Detect any pairs of balls that are colliding.
#     Returns a set of ball_pairs.
#     """
#
#     set_of_collisions = set()
#
#     for i in range(len(balls)):
#         b1 = balls[i]
#         for j in range(i):
#             b2 = balls[j]
#             if gas.colliding(b1, b2):
#                 set_of_collisions.add(gas.ball_pair(b1, b2))
#
#     return set_of_collisions

import gas

