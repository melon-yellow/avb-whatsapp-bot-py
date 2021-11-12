
##########################################################################################################################

# Imports
import json
import requests
import datetime

##########################################################################################################################

# PyMes Function
def py_check(tagname: str):
    try: # Request IP21 Server
        req = requests.post(
            'http://avbsrvssta:3002/api2/ip21/',
            json = dict(tagname = tagname),
            auth = ('client', '#22gh3er41ty2q@ewe3e9u')
        )
        res: dict = json.loads(req.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='Server Down')
    # Return data
    return res

##########################################################################################################################

# Last Update
lastupdate = None

# Data Variables
cimios = dict(
    AFS = None,
    BOF = None,
    LCFP = None
)

# Fault Gone
fault = dict(
    AFS = False,
    BOF = False,
    LCFP = False
)

##########################################################################################################################

# Convert
def conv(ip_value: str):
    if not isinstance(ip_value, str): return
    try:
        return datetime.datetime.strptime(
            ip_value, '%d/%m/%Y %H:%M:%S'
        )
    except: return

##########################################################################################################################

# Update Timestamps
def update():
    # Get Cim-IO Timestamps
    afs = conv(py_check('IP21@CIMIO_AFS_T-R').get('value'))
    bof = conv(py_check('IP21@CIMIO_BOF_T-R').get('value'))
    lcfp = conv(py_check('IP21@CIMIO_LCFP_T-R').get('value'))
    # Assign Values
    if afs != None: cimios['AFS'] = afs + datetime.timedelta(minutes = 7)
    if bof != None: cimios['BOF'] = bof + datetime.timedelta(minutes = 1)
    if lcfp != None: cimios['LCFP'] = lcfp + datetime.timedelta(minutes = -3)
    # Set Last Update
    lastupdate = datetime.datetime.now()

##########################################################################################################################

# Check Method
def check(ts: datetime.datetime):
    if ts == None: return False
    if lastupdate > ts: dif = lastupdate - ts
    else: dif = ts - lastupdate
    m3 = datetime.timedelta(minutes = 3)
    if dif.seconds > m3.seconds: return False
    return True

##########################################################################################################################

# Check If Cim-IO is OK
def nok(key: str):
    return not check(cimios.get(key))

##########################################################################################################################
