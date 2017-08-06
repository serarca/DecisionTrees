# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import copy

# Receives a list of dictionaries, each dictionary has a weight and a set
# Also receives a universe
def set_cover(sets, weights, universe):
    ss = copy.deepcopy(sets)
    ws = copy.deepcopy(weights)
    u = copy.deepcopy(universe)
    selection = np.zeros(len(ss))
    k = 1
    while(len(u)!= 0):
        min_cost = float('inf')
        print(len(u))
        min_index = -1
        for i,s in enumerate(ss):
            if (len(s) > 0):
                cost = ws[i]/len(s)
                if (cost < min_cost):
                    min_index = i
                    min_cost = cost
        if (min_index == -1):
            break
        else:
            selection[min_index] = k
            k += 1
            selected_set = ss[min_index]
            u = [x for x in u if x not in selected_set]
            for i,s in enumerate(ss):
                ss[i] = [x for x in s if x not in selected_set]
    if (len(u)!= 0):
        print("universe not empty")
    return selection 

