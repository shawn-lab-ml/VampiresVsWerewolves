import config as cfg
import random

######################## THIS SECTION IS RELATED TO DISTANCE CALCULATIONS ################################

def distance_player(player1, player2):

    """
    :param player1: dictionary of player 1 states
    :param player2: dictionary of player 2 states
    :return: distance (sorted) - list of list of ints,
            positions - list of list of positions,
            quantities - list of list of ints
    """

    total_distances = []
    total_positions = []
    total_quantities = []

    for (xP1, yP1) in player1.keys():
        distances = []
        positions = []
        quantities = []

        for (xP2, yP2) in player2.keys():
            distances.append(manhattan_distance(xP1, xP2, yP1, yP2))
            positions.append((xP2, yP2))
            quantities.append(player2[xP2,yP2])

        # sorting with respect to distances

        if distances:
            distances, positions, quantities = zip(*sorted(zip(distances, positions, quantities)))

            total_distances.append(list(distances))
            total_positions.append(list(positions))
            total_quantities.append(list(quantities))

        else:
            total_distances.append([0])
            total_positions.append([])
            total_quantities.append([0])


    return total_distances, total_positions, total_quantities

def manhattan_distance(xP1, xP2, yP1, yP2):
    return max(abs((xP1 - xP2)), abs((yP1 - yP2)))

def euclidean_distance(xP1, xP2, yP1, yP2):
    return max((xP1 - xP2)**2, (yP1 - yP2)**2)



######################## THIS SECTION IS RELATED TO OCCUPATION OF CELL ################################

def enemy_in_cell(us, enemy, x, y, x_update, y_update, q1):


    """
    :param us: our state
    :param enemy: the enemy's state
    :param x: the initial position
    :param y: the initial position
    :param x_update: the position of interest
    :param y_update: the position of interest
    :param q1: quantity displaced by us
    :return:
    """

    p = 1

    q2 = enemy[(x_update, y_update)]

    # If the difference is 1.5 times higher or 1.5 times lower then no randomness
    if 1.5*q2 <= q1:
        us[(x_update, y_update)] = q1
        del enemy[(x_update, y_update)]

        if q1 == us[(x,y)]:
            del us[(x, y)]
        else:
            us[(x, y)] -= q1

    elif q2 >= 1.5 * q1:

        if q1 == us[(x,y)]:
            del us[(x, y)]
        else:
            us[(x, y)] -= q1

    # Else, a random battle starts:
    # If we are more we win and keep p*initial number of creatures
    # If we are less we lose and the enemy keeps (1-p) * inital number of creatures
    # Implemented this as we are looking at the expected gains: p*Initial_number + 0*(1-p)

    else:
        (q1_temp, q2_temp), p = random_battle(q1, q2)

        if q1_temp != 0:
            us[(x_update, y_update)] = q1_temp
            del enemy[(x_update, y_update)]

            if q1 == us[(x,y)]:
                del us[(x, y)]

            else:
                us[(x, y)] -= q1

        else:
            enemy[(x_update, y_update)] = q2_temp

            if q1 == us[(x,y)]:
                del us[(x, y)]

            else:
                us[(x, y)] -= q1

    return us, enemy, p


def human_in_cell(us, human, x, y, x_update, y_update, q1):

    """
    :param us: our state
    :param human: human state
    :param x: initial position
    :param y: initial position
    :param x_update: position of interest
    :param y_update: position of interest
    :param q1: quantity displaced by us
    :return:
    """

    # straightforward: if we are more or equal to humans then we gain them

    if human[(x_update, y_update)] <= q1:
        us[(x_update, y_update)] = human[(x_update, y_update)] + q1
        del human[(x_update, y_update)]

    if us[(x, y)] == q1:
        del us[(x, y)]

    else:
        us[(x, y)] -= q1

    return us, human


def us_in_cell(us, x,y,  x_update, y_update, q1):
    """
    :param us: our state
    :param x: initial position
    :param y: initial position
    :param x_update: position of interest
    :param y_update: position of interest
    :param q1: quantity displaced by us
    :return:
    """

    if q1 == us[(x,y)]:
        us[(x_update, y_update)] += q1
        del us[(x,y)]

    else:
        us[(x_update, y_update)] += q1
        us[(x, y)] -= q1

    return us


def random_battle(a, b):  # a: qte attacking. b:qte de l'autre espece. specie: human or monstre
    if a == b:
        p = 0.5
        a = 0
        b = 0

    elif a < b:
        p = a / (2 * b)

        a *= 0  # chacun a une probabilite p de survivre donc a devient p*a

        b *= (1-p)

    else:
        p = (a / b) - 0.5

        a *= p
        b = 0 # chaque enemy a une proba (1-p) de survivre

    return (a, b), p


######################## THIS SECTION IS RELATED TO THE MOVEMENT RULES ################################


def isLegalMove(x,y):
    if (x < 0) or (x > cfg.X_LIM - 1):
        return False

    if (y < 0) or (y > cfg.Y_LIM - 1):
        return False

    return True


def flee(xP1, yP1, xP2, yP2):

    """
    :param xP1: x position of Us
    :param yP1: y position of Us
    :param xP2: x position of Enemy
    :param yP2: y position of Enemy
    :return: the optimal position to run away from the enemy
    """

    if xP1 < xP2 and isLegalMove(xP1 - 1, yP1):
        x_update = xP1 - 1

    elif xP1 > xP2 and isLegalMove(xP1 + 1, yP1):
        x_update = xP1 + 1

    else: x_update = xP1

    if yP1 <= yP2 and isLegalMove(x_update, yP1 - 1):
        y_update = yP1 - 1

    elif yP1 >= yP2 and isLegalMove(x_update, yP1 + 1):
        y_update = yP1 + 1

    else: y_update = yP1

    return (x_update, y_update)

def moveTowards(xP1, yP1, xP2, yP2):

    """
    :param xP1: x position of Us
    :param yP1: y position of Us
    :param xP2: x position of Enemy
    :param yP2: y position of Enemy
    :return: the optimal position to run away from the enemy
    """

    if xP1 < xP2:
        x_update = xP1 + 1

    elif xP1 > xP2:
        x_update = xP1 - 1

    else:
        x_update = xP1

    if yP1 < yP2:
        y_update = yP1 + 1

    elif yP1 > yP2:
        y_update = yP1 - 1

    else:
        y_update = yP1

    return (x_update, y_update)


######################## THIS SECTION IS RELATED TO THE POSSIBLE MOVEMENTS ################################

"""def move_wrt_human_2_groups(us, human, hum_grps):


    :param us: our state
    :param human: human state
    :param hum_grps: number of groups considered in our calculations
    :return:

    dH, pH, qH = distance_player(us, human)
    [(xUs1, yUs1), (xUs2, yUs2)] = list(us.keys())

    mov1 = []
    mov2 = []

    for i, (xH1, yH1) in enumerate(pH[0]):

        if len(mov1) == hum_grps and len(mov2) == hum_grps:
            break

        for j, (xH2, yH2) in enumerate(pH[1]):

            if qH[0][i] > us[(xUs1, yUs1)] or qH[0][i] == 0:
                break

            elif ~ (qH[1][j] > us[(xUs2, yUs2)] or qH[1][j] == 0):

                if len(mov1) < hum_grps:
                    x_update, y_update = moveTowards(xUs2, yUs2, xH2, yH2)
                    mov1.append((xUs2, yUs2, us[(xUs2, yUs2)], x_update, y_update))

                if len(mov2) < hum_grps:
                    x_update, y_update = moveTowards(xUs1, yUs1, xH1, yH1)
                    mov2.append((xUs1, yUs1, us[(xUs1, yUs1)], x_update, y_update))

            elif len(mov1) < hum_grps:
                x_update, y_update = moveTowards(xUs1, yUs1, xH1, yH1)
                mov2.append((xUs1, yUs1, us[(xUs1, yUs1)], x_update, y_update))

            if len(mov1) == hum_grps and len(mov2) == hum_grps:
                break

    return mov1, mov2"""



def move_wrt_human(qUs, xUs, yUs, pH, qH, n_groups, is_2_groups = True):

    """
    :param qUs: quantity of us in the group
    :param xUs: our posiiton
    :param yUs: our position
    :param pH: positions of the humans
    :param qH: quantity of humans
    :param n_groups: number of groups that are considered to compute the possible moves
    :return: the moves related to moving towards the human. When we only have one group the split must be considered as well
    """

    count = 0
    moves = set()
    nh_associated_move = {}

    for k, (xH, yH) in enumerate(pH[0]):

        # for the closest humans that is less than us move towards
        if count == n_groups:
            break

        if qH[0][k] <= qUs:
            count += 1

            (x_update, y_update) = moveTowards(xUs, yUs, xH, yH)

            moves.add((xUs, yUs, qUs, x_update, y_update))

            if ~is_2_groups:
                nh_associated_move[(x_update, y_update)] = qH[0][k]

    if is_2_groups:
        return moves

    else:

        if len(moves) > 1:
            temp_moves = set()

            for idx1 in range(len(moves) - 1):
                x1_update, y1_update = list(moves)[idx1][3:]

                for idx2 in range(idx1, len(moves)):
                    x2_update, y2_update = list(moves)[idx2][3:]

                    # don't want to check splitting when moving in the same direction
                    if abs(x1_update - x2_update) + abs(y1_update - y2_update) > 0:
                        nh = nh_associated_move[(x1_update, y1_update)] + nh_associated_move[(x2_update, y2_update)]

                        if nh <= qUs:
                            r1 = qUs - nh
                            r2 = r1 - r1 // 2

                            move = ((xUs, yUs, nh_associated_move[(x1_update, y1_update)] + r1 // 2, x1_update, y1_update),
                                                     (xUs, yUs, nh_associated_move[(x2_update, y2_update)] + r2, x2_update, y2_update))

                            temp_moves.add(tuple(sorted(move)))
            moves = set.union(moves, temp_moves)

        return moves

def move_wrt_enemy(qUs, xUs, yUs, pE, n_groups):

    """
    :param qUs: quantity of us in the group
    :param xUs: our posiiton
    :param yUs: our position
    :param pH: positions of the humans
    :param qH: quantity of humans
    :param n_groups: number of groups that are considered to compute the possible moves
    :return: the moves related to moving towards the enemy
    """

    moves = set()
    count = 0
    # for each enemy either move Towards or flee
    for k, (xE, yE) in enumerate(pE[0]):

        if count == n_groups:
            break

        if (xUs, yUs) != flee(xUs, yUs, xE, yE):

            (x_update, y_update) = flee(xUs, yUs, xE, yE)
            moves.add((xUs, yUs, qUs, x_update, y_update))

        (x_update, y_update) = moveTowards(xUs, yUs, xE, yE)

        moves.add((xUs, yUs, qUs, x_update, y_update))

        count += 1

    return moves

def merge_groups(xUs1, yUs1, qUs1, xUs2, yUs2, qUs2):

    moves = set()
    x1_update, y1_update = moveTowards(xUs1, yUs1, xUs2, yUs2)

    if x1_update == xUs2 and y1_update == yUs2:
        moves.add((xUs1, yUs1, qUs1, xUs2, yUs2))

    else:
        x2_update, y2_update = moveTowards(xUs2, yUs2, x1_update, y1_update)

        move = ((xUs1, yUs1, qUs1, x1_update, y1_update),
                 (xUs2, yUs2, qUs2, x2_update, y2_update))

        moves.add(tuple(sorted(move)))

    return moves


def move_2_groups(us, enemy, human):
    """
    :param us: our states
    :param enemy: enemy states
    :param human: human states
    :return: possible moves when we have 2 groups on the map
    """

    possibleMoves = set()
    [(xUs1, yUs1), (xUs2, yUs2)] = list(us.keys())
    qUs1 = us[(xUs1, yUs1)]
    qUs2 = us[(xUs2, yUs2)]

    # attack humans
    # moving towards the 3 closest humans

    if human:
        dH, pH, qH = distance_player(us, human)

        mov1 = move_wrt_human(qUs1, xUs1, yUs1, pH, qH, 3)
        mov2 = move_wrt_human(qUs2, xUs2, yUs2, pH, qH, 3)

        # permutations of the possible moves and sorting to avoid
        # having suplicates in the set

        for elem1 in mov1:
            for elem2 in mov2:
                possibleMoves.add(tuple(sorted((elem1, elem2))))


    # attack enemies / flee

    if enemy:
        dE, pE, qE = distance_player(us, enemy)

        mov1 = move_wrt_enemy(qUs1, xUs1, yUs1, pE, 2)
        mov2 = move_wrt_enemy(qUs2, xUs2, yUs2, pE, 2)

        for elem1 in mov1:
            for elem2 in mov2:
                possibleMoves.add(tuple(sorted((elem1, elem2))))


    # Merging both groups

    moves = merge_groups(xUs1, yUs1, qUs1, xUs2, yUs2, qUs2)

    possibleMoves = set.union(possibleMoves, moves)

    return possibleMoves


def move_2_groups_start(us, human):
    """
    :param us: our state
    :param enemy: the enemy state
    :param human: the human state
    :return: the best possible list of moves at the start of the game
    """

    possibleMoves = set()
    [(xUs1, yUs1), (xUs2, yUs2)] = list(us.keys())


    # attack humans
    # moving towards the 2 closest humans

    if human:
        dH, pH, qH = distance_player(us, human)

        qUs1 = us[(xUs1, yUs1)]
        qUs2 = us[(xUs2, yUs2)]

        mov1 = move_wrt_human(qUs1, xUs1, yUs1, pH, qH, 3)
        mov2 = move_wrt_human(qUs2, xUs2, yUs2, pH, qH, 3)

        # permutations of the possible moves and sorting to avoid
        # having suplicates in the set

        for elem1 in mov1:
            for elem2 in mov2:
                possibleMoves.add(tuple(sorted((elem1, elem2))))

    # Merging both groups

    moves = merge_groups(xUs1, yUs1, qUs1, xUs2, yUs2, qUs2)

    possibleMoves = set.union(possibleMoves, moves)

    return possibleMoves


def move_1_group(us, enemy, human):

    """
    :param us: our state
    :param enemy: the enemy state
    :param human: the human state
    :return: the best possible moves for a single group
    """

    possibleMoves = set()

    (xUs, yUs) = list(us.keys())[0]
    qUs = us[(xUs, yUs)]

    if human:
        dH, pH, qH = distance_player(us, human)
        possibleMoves = move_wrt_human(qUs, xUs, yUs, pH, qH, 4, False)

    if enemy:
        dE, pE, qE = distance_player(us, enemy)

        moves = move_wrt_enemy(qUs, xUs, yUs, pE, 2)

        possibleMoves = set.union(possibleMoves, moves)

    return possibleMoves



def move_1_group_start(us, human):
    possibleMoves = set()

    (xUs, yUs) = list(us.keys())[0]
    qUs = us[(xUs, yUs)]

    if human:
        dH, pH, qH = distance_player(us, human)
        possibleMoves = move_wrt_human(qUs, xUs, yUs, pH, qH, 4, False)

    return possibleMoves



def compute_possible_moves(us, enemy, human, isEnemy = False):

    """
    :param us: player 1 state
    :param enemy: player 2 state
    :param human: human state
    :param isEnemy: refers to wether it is the minimization turn to play as we always want to be wary of getting close to ennemies
    :return: list of possible moves

    This function will compute the possible moves with regards to the enemy's positions,
    the human's positions (the 5 nearest), the possibility to split or merge, and the
    combination of these when there are at least 2 groups.
    """

    HUM_THRESH = 4
    ENEMY_THRESH = 2

    num_e = len(enemy)
    num_h = len(human)
    num_u  = len(us)

    possible = False

    for elem in list(human.values()):
        if elem < sum(us.values()):
            possible = True


    # if there are few humans then consider the ennemies

    if ((num_h < HUM_THRESH or possible == False) and (num_e < ENEMY_THRESH)) or (isEnemy == True and num_h < HUM_THRESH):

        if ~isEnemy:
            cfg.MAX_DEPTH = 7

        if num_u == cfg.MAX_GROUPS:
            possibleMoves = move_2_groups(us, enemy, human)

        else:
            possibleMoves = move_1_group(us, enemy, human)

    # if there are few humans and many enemies lower the depth
    elif (num_h < HUM_THRESH or possible == False or isEnemy == True) and num_e >= ENEMY_THRESH:

        if ~isEnemy:
            cfg.MAX_DEPTH = 6

        if num_u == cfg.MAX_GROUPS:
            possibleMoves = move_2_groups(us, enemy, human)

        else:
            possibleMoves = move_1_group(us, enemy, human)


    # when many humans just consider humans and go deeper
    else:

        cfg.MAX_DEPTH = 7

        if num_u == cfg.MAX_GROUPS:
            possibleMoves = move_2_groups_start(us, human)

        else:
            possibleMoves = move_1_group_start(us, human)


    possibleMoves = list(possibleMoves)
    random.shuffle(possibleMoves)

    return possibleMoves