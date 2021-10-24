
##########################################################################################################################

import py_misc

##########################################################################################################################
#                                                      CLASSE IBA PDA                                                    #
##########################################################################################################################

# Laminador Class
class PDA:

    def __init__(
        self,
        misc: py_misc,
        pda_db: py_misc.MySQL
    ):
        self.misc = misc
        self.db = pda_db

    # Get Timestamp from IBA
    def timestamp(self, t):
        kwargs = dict(microsecond=(t[0]*1000), second=t[1],
            minute=t[2], hour=t[3], day=t[4], month=t[5], year=t[6])
        timestamp = self.misc.datetime.datetime(**kwargs)
        return timestamp

##########################################################################################################################
