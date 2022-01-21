import utils
import config as cfg
import copy

MAX, MIN = 10000, -10000
WIN_SCORE = 20
LOSE_SCORE = -1000
DISCOUNT = 0.95


def run_minimax(state):
    """
    :param state: states of the map
    :return: best score and best move

    the summary dictionary is used to weight the actions by the time and the randomness
    """

    best_move = 0

    states = state.getState()

    summary = {
        'UsIncrease': 0,
        'EnemyIncrease': 0,
        'proba_rg': 1,
        'discount': 1
    }

    best, best_move = minimax(states = states, depth = 0, maximizingPlayer = True,
            alpha = -float('inf'), beta = float('inf'),
            best_move=best_move, summary = summary)

    return best, best_move

# Returns optimal value for current player
# (Initially called for root and maximizer)

def maximizer(states, move, summary):

    (us, enemy, human) = (states[0], states[1], states[2])
    x, y, qU, x_update, y_update = move
    p = 1

    # verifying if humans in cell, if so, check the quantity of humans vs the player's
    if (x_update, y_update) in human:
        us, human = utils.human_in_cell(us, human, x, y, x_update, y_update, qU)

        if (x_update, y_update) in us:
            summary['UsIncrease'] += (us[(x_update, y_update)] - qU) * summary['discount']

        else:
            summary['UsIncrease'] -= qU * summary['discount']

    # verifying if enemy in cell, if so, check the quantity of humans vs the player's
    elif (x_update, y_update) in enemy:
        qE = enemy[(x_update, y_update)]
        us, enemy, p = utils.enemy_in_cell(us, enemy, x, y, x_update, y_update, qU)

        if (x_update, y_update) in us:
            summary['UsIncrease'] += (us[(x_update, y_update)] - qU) * summary['discount']
            summary['EnemyIncrease'] -= qE * summary['discount']

        else:
            summary['EnemyIncrease'] += (enemy[(x_update, y_update)]-qE) * summary['discount']
            summary['UsIncrease'] -= qU * summary['discount']


    elif (x_update, y_update) in us:
        us= utils.us_in_cell(us, x, y, x_update, y_update, qU)

    else:
        us[(x_update,y_update)] = qU

        if qU != us[(x,y)]:
            us[(x,y)] -= qU

        else:
            del us[(x,y)]

    summary['proba_rg'] *= p

    return (us, enemy, human), summary


def minimizer(states, move, summary):

    (us, enemy, human) = (states[0], states[1], states[2])
    x, y, qE, x_update, y_update = move

    p = 1

    if (x_update, y_update) in human:
        enemy, human = utils.human_in_cell(enemy, human, x, y, x_update, y_update, qE)

        if (x_update, y_update) in enemy:
            summary['EnemyIncrease'] += (enemy[(x_update, y_update)] - qE) * summary['discount']

        else:
            summary['EnemyIncrease'] -= qE * summary['discount']

    elif (x_update, y_update) in us:
        qU = us[(x_update, y_update)]

        enemy, us, p = utils.enemy_in_cell(enemy, us, x, y, x_update, y_update, qE)

        if (x_update, y_update) in enemy:
            summary['EnemyIncrease'] += (enemy[(x_update, y_update)] - qE) * summary['discount']
            summary['UsIncrease'] -= qU * summary['discount']

        else:
            summary['UsIncrease'] += (us[(x_update, y_update)] -qU) * summary['discount']
            summary['EnemyIncrease'] -= qE * summary['discount']

    elif (x_update, y_update) in enemy:
        enemy = utils.us_in_cell(enemy, x, y, x_update, y_update, qE)

    else:
        enemy[(x_update,y_update)] = qE

        if qE != enemy[(x,y)]:
            enemy[(x, y)] -= qE

        else: del enemy[(x,y)]

    summary['discount'] *= DISCOUNT
    summary['proba_rg'] *= p

    return (us, enemy, human), summary


def minimax(states, depth, maximizingPlayer, alpha, beta, best_move, summary):

    """
    states : human, enemy, us dictionary
    depth : 0 in the beginning and increments by one at each iteration
    maximizingPlayer: bool True when it is our turn (i.e. we maximize our gains)
    alpha : -inf in the beginning but is updated by the minimizer
    Beta : inf in the beginning but is updated by the maximizer
    best_move : 0 in the beginning and then takes the best move : (x, y, qU, x_update, y_update)
    """

    # Terminating condition. i.e
    # leaf node is reached
    # copying states at each iteration
    (us_temp, enemy_temp, human_temp) = (states[0], states[1], states[2])
    summary_temp = copy.deepcopy(summary)

    if depth >= cfg.MAX_DEPTH:

        dist = 0

        if sum(human_temp.values()) != 0:

            dH, pH, qH = utils.distance_player(us_temp, human_temp)

            if len(us_temp) == cfg.MAX_GROUPS:

                if len(pH[0]) > 2:

                    if pH[0][0] == pH[1][0]:

                        if dH[0][0] <= dH[1][0]:
                            dist1, dist2 = dH[0][0], dH[1][1]

                        else:
                            dist1, dist2 = dH[0][1], dH[1][0]

                        dist = dist1 + dist2

                else:
                    dist = dH[0][0] * 2

                [(xUs1, yUs1), (xUs2, yUs2)] = list(us_temp.keys())

                intra_dist = utils.manhattan_distance(xUs1,xUs2, yUs1, yUs2)

                return (summary_temp['UsIncrease'] - 0.9*summary_temp['EnemyIncrease'] - 1.1*sum(human_temp.values()) - (0.1*dist/8) - 1/intra_dist), best_move


            else:

                for i, quant in enumerate(qH[0]):
                    if quant <= int(list(us_temp.values())[0]):
                        dist = dH[0][i]
                        break

                return (summary_temp['UsIncrease'] - 0.9*summary_temp['EnemyIncrease'] - 1.1*sum(human_temp.values()) - 0.1*dist), best_move

        dE, pE, qE = utils.distance_player(us_temp, enemy_temp)

        for i, elem in enumerate(dE[0]):
            if qE[0][i] < int(list(us_temp.values())[0]):
                dist = elem
                break

        return (summary_temp['UsIncrease'] - 1.2 * summary_temp['EnemyIncrease'] - 2*len(us_temp) - dist), best_move

    if maximizingPlayer:
        moves = utils.compute_possible_moves(us_temp, enemy_temp, human_temp, isEnemy=True)

        best = MIN

        # for each possible move
        for i in range(0, len(moves)):

            # copying states
            states_temp = (states[0].copy(), states[1].copy(), states[2].copy())
            summary_temp = copy.copy(summary)

            if len(moves[i]) == 2:
                for m in moves[i]:
                    states_temp, summary_temp = maximizer(states_temp, m, summary_temp)

            else:
                states_temp, summary_temp = maximizer(states_temp, moves[i],summary_temp)

            if not states_temp[0]:
                score = LOSE_SCORE*summary_temp['proba_rg']*summary_temp['discount']

            elif not states_temp[1]:
                score = (WIN_SCORE + sum(us_temp.values())) *summary_temp['proba_rg']*summary_temp['discount']

            else:
                score, best_move = minimax(states_temp, depth + 1, False, alpha, beta, best_move,summary_temp)


            if depth == 0:
                if score > best:
                    best_move = moves[i]

            best = max(best, score)
            alpha = max(alpha, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best, best_move

    else:

        best = MAX

        # switched enemy and us as we want to possible moves for the enemy
        moves = utils.compute_possible_moves(enemy_temp, us_temp, human_temp)

        for i in range(0, len(moves)):

            states_temp = (states[0].copy(), states[1].copy(), states[2].copy())
            summary_temp = copy.copy(summary)

            if len(moves[i]) == 2:
                for m in moves[i]:
                    states_temp, summary_temp = minimizer(states_temp, m, summary_temp)

            else:
                states_temp, summary_temp = minimizer(states_temp, moves[i],summary_temp)


            if not states_temp[0]:
                score = LOSE_SCORE*summary_temp['proba_rg']*summary_temp['discount']

            elif not states_temp[1]:
                score = (WIN_SCORE + sum(enemy_temp.values()))*summary_temp['proba_rg']*summary_temp['discount']

            else:
                score, _ = minimax(states_temp, depth + 1,True, alpha, beta, best_move, summary_temp)

            best = min(best, score)
            beta = min(beta, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best, best_move