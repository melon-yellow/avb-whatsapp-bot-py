##########################################################################################################################
#                                                           PY-MES                                                       #
##########################################################################################################################

# PyMes Function
def py_check(tagname):
    try: # Request IP21 Server
        res = Avbot.bot.misc.requests.post(
            'http://avbsrvssta:3002/api2/ip21/',
            json = dict(tagname = tagname),
            auth = ('client', '#22gh3er41ty2q@ewe3e9u')
        )
        res = Avbot.bot.misc.json.loads(res.text)
    except: # If Server Not Responding
        res = dict(value=None, name=None, status='Server Down')
    # Return data
    return res


