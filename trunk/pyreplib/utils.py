from pyreplib import actions

def avg(L):
    if L:
        return sum(L) / float(len(L))

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
            n = 1
            minute += one_minute
    yield n

def apm_stats(player):
    '''
    Return the minimum, average and maximum number of actions
    per minutes for `player`.
    '''
    actions = list(actions_per_minute(player))
    return (min(actions),
            round(avg(actions)),
            max(actions))

def unit_distribution(player):
    '''
    Return a dictionary containing the unit types and the number produced
    during the game for `player`.
    '''
    distribution = {}
    for action in player.actions:
        # Protoss and Terrans train, Zerg hatch.
        if isinstance(action, (actions.Train, actions.Hatch)):
            unit_name = action.get_unit_type()
            distribution[unit_name] = 1 + distribution.get(unit_name, 0)
    return distribution

def building_distribution(player):
    '''
    Return a dictionary containing the building types and the number produced
    during the game for `player`.
    '''
    distribution = {}
    for action in player.actions:
        # Protoss, Terrans and Zerg build, Zerg also morph.
        if isinstance(action, (actions.Build, actions.Morph)):
            building_name = action.get_building_type()
            distribution[building_name] = 1 + distribution.get(building_name, 0)
    return distribution
