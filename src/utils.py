from src.random_vars import uniform
def harbor_active(ship_info):
    if len(ship_info) == 0:
        return True
    for ship in ship_info.keys():
        if ship_info[ship][1] is None:
            return True
    return False


def choose_boat():
    x = uniform()
    if x <= 0.25:
        return 'small'
    elif x <= (0.25 + 0.25):
        return 'medium'
    else:
        return 'large'
    
def choose_dock(docks):
    if docks[0] is None:
        return 0
                    
    elif docks[1] is None:
        return 1
    elif docks[2] is None:
        return 2
    else: 
        return None

def find_ship_ready(depart_time,docks):
    d = min(depart_time)
    indx = depart_time.index(d)
    return docks[indx],indx