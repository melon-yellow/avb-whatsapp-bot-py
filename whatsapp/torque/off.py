
##########################################################################################################################

import copy
import datetime
from py_wapp import Bot

##########################################################################################################################

# Data Variables
stds = [
    [],[],[],[],[],[],
    [],[],[],[],[],[],
    [],[],[],[],[],[]
]

##########################################################################################################################

# Clear Torque
def clear():
    t = datetime.datetime.now()
    for item in stds:
        temp = copy.deepcopy(item)
        for e in item:
            t1 = t - datetime.timedelta(hours=1)
            if e <= t1: del temp[temp.index(e)]
        stds[stds.index(item)] = temp
        
##########################################################################################################################

# Add Torque
def add(std: int):
    clear()
    offset = std - 1
    t = datetime.datetime.now()
    stds[offset].append(t)
    return len(stds[offset]) == 1

##########################################################################################################################

# Torque Off
def enum():
    clear()
    cond = False
    off = list()
    for item in stds:
        i = stds.index(item)
        if len(item) > 0:
            off.append(
                dict(
                    std=(i + 1),
                    stamps=item,
                    times=len(item)
                )
            )
        if len(item) > 1: cond = True
    return dict(off=off, cond=cond)

##########################################################################################################################

# Torque Anormal Ultima Hora
def send(bot: Bot):
    m = enum()
    if type(m) != dict: return False
    if not m['cond']: return False
    m = m['off']
    msg = ' '.join(('Na ultima hora os torques das',
        'seguintes gaiolas ficaram fora do normal:'))
    for i in m:
        msg += f'\nGaiola {i["std"]}: {i["times"]} vezes'
    # send message
    bot.send(to='anthony', text=msg, log='api::pda_mill_m_off(scheduled)')

##########################################################################################################################
