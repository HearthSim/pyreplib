def avg(L):
    if not L:
        return 0
    else:
        return sum(L) / len(L)

def actions_per_minute(player):
    '''
    Yield the number of actions for each minute of the game for `player`.
    '''
    one_minute = 24 * 60
    minute = one_minute
    n = 0
    for action in player.actions:
        if action.tick < minute:
            n += 1
        else:
            yield n
            n = 0
            minute += one_minute

def apm_stats(player):
    '''
    Return the minimum, average and maximum number of actions
    per minutes for `player`.
    '''
    actions = list(actions_per_minute(player))
    return (min(actions),
            avg(actions),
            max(actions))
