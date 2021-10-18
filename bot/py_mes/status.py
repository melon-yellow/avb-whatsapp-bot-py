##########################################################################################################################
#                                                   ONE MINUTE SCHEDULE                                                  #
##########################################################################################################################

# Class Torque Off
class PyMESCheck:

    def __init__(self):
        # Data Variables
        self.cimios = dict(
            AFS = None,
            BOF = None,
            LCFP = None
        )
        self.fault = dict(
            AFS = False,
            BOF = False,
            LCFP = False
        )

    @property
    def bot(self): return Avbot.bot

    # Convert
    def conv(self, ip_value):
        if not isinstance(ip_value, str): return None
        try:
            return self.bot.misc.datetime.datetime.strptime(
                ip_value, '%d/%m/%Y %H:%M:%S'
            )
        except Exception as e:
            print(e)
            return None

    # Update Timestamps
    def update(self):
        # Get Cim-IO Timestamps
        afs = self.conv(py_check('IP21@CIMIO_AFS_T-R').get('value'))
        bof = self.conv(py_check('IP21@CIMIO_BOF_T-R').get('value'))
        lcfp = self.conv(py_check('IP21@CIMIO_LCFP_T-R').get('value'))

        # Assign Values
        if afs != None: self.cimios['AFS'] = afs + Avbot.bot.misc.datetime.timedelta(minutes = 7)
        if bof != None: self.cimios['BOF'] = bof + Avbot.bot.misc.datetime.timedelta(minutes = 1)
        if lcfp != None: self.cimios['LCFP'] = lcfp + Avbot.bot.misc.datetime.timedelta(minutes = -3)

        # Set Last Update
        self.lastupdate = self.bot.misc.datetime.datetime.now()
    
    # Check Method
    def check(self, dt):
        if dt == None: return False
        if self.lastupdate > dt: dif = self.lastupdate - dt
        else: dif = dt - self.lastupdate
        m3 = self.bot.misc.datetime.timedelta(minutes = 3)
        if dif.seconds > m3.seconds:
            return False
        return True
    
    # Check If Cim-IO is OK
    def nok(self, key):
        return not self.check(self.cimios.get(key))

# Instance Object
pyMesCheck = PyMESCheck()