
##########################################################################################################################

import py_misc

##########################################################################################################################
#                                                           PY-MES                                                       #
##########################################################################################################################

# PyMes Function
def py_check(misc: py_misc, tagname: str):
    try: # Request IP21 Server
        res = misc.requests.post(
            'http://avbsrvssta:3002/api2/ip21/',
            json = dict(tagname = tagname),
            auth = ('client', '#22gh3er41ty2q@ewe3e9u')
        )
        res = misc.json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='Server Down')
    # Return data
    return res

##########################################################################################################################
#                                                           PY-MES                                                       #
##########################################################################################################################

# Class Torque Off
class PyMESCheck:

    # Init Py-Mes Check
    def __init__(self, misc: py_misc):
        
        # Reference Bot
        self.misc = misc
        
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

    # Convert
    def conv(self, ip_value):
        if not isinstance(ip_value, str): return None
        try:
            return self.misc.datetime.datetime.strptime(
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
        if afs != None: self.cimios['AFS'] = afs + self.misc.datetime.timedelta(minutes = 7)
        if bof != None: self.cimios['BOF'] = bof + self.misc.datetime.timedelta(minutes = 1)
        if lcfp != None: self.cimios['LCFP'] = lcfp + self.misc.datetime.timedelta(minutes = -3)

        # Set Last Update
        self.lastupdate = self.misc.datetime.datetime.now()
    
    # Check Method
    def check(self, dt):
        if dt == None: return False
        if self.lastupdate > dt: dif = self.lastupdate - dt
        else: dif = dt - self.lastupdate
        m3 = self.misc.datetime.timedelta(minutes = 3)
        if dif.seconds > m3.seconds:
            return False
        return True
    
    # Check If Cim-IO is OK
    def nok(self, key):
        return not self.check(self.cimios.get(key))

##########################################################################################################################
