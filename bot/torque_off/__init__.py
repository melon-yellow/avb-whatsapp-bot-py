
##########################################################################################################################

from py_wapp import Bot

##########################################################################################################################
#                                                      CLASSE TORQUE OFF                                                 #
##########################################################################################################################

# Class Torque Off
class TorqueOff:

    def __init__(self, bot: Bot):
        # Reference Bot
        self.bot = bot
        # Data Variables
        self.s = [
            [],[],[],[],[],[],
            [],[],[],[],[],[],
            [],[],[],[],[],[]
        ]
    
    @property
    def misc(self):
        return self.bot.misc

    # Clear Torque
    def clear(self):
        t = self.misc.datetime.datetime.now()
        for item in self.s:
            temp = self.misc.copy.deepcopy(item)
            for e in item:
                t1 = t - self.misc.datetime.timedelta(hours=1)
                if e <= t1: del temp[temp.index(e)]
            self.s[self.s.index(item)] = temp

    # Add Torque
    def add(self, std):
        self.clear()
        offset = std-1
        t = self.misc.datetime.datetime.now()
        self.s[offset].append(t)
        return len(self.s[offset]) == 1

    # Torque Off
    @property
    def off(self):
        self.clear()
        cond = False
        off = list()
        for item in self.s:
            i = self.s.index(item)
            if len(item) > 0:
                off.append(dict(std=(i+1),
                stamps=item, times=len(item)))
            if len(item) > 1: cond = True
        return dict(off=off, cond=cond)

    # Torque Anormal Ultima Hora
    def send_off(self):
        m = self.off
        if type(m) != dict: return False
        if not m['cond']: return False
        m = m['off']
        msg = ' '.join(('Na ultima hora os torques das',
            'seguintes gaiolas ficaram fora do normal:'))
        for i in m:
            msg += '\nGaiola {}: {} vezes'.format(i['std'], i['times'])
        # send message
        self.bot.send('anthony', msg, 'api::pda_mill_m_off(scheduled)')
        
##########################################################################################################################
