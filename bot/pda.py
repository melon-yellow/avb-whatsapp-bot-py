##########################################################################################################################
#                                                      CLASSE IBA PDA                                                    #
##########################################################################################################################

# Laminador Class
class PDA:

    iba_db = iba_db

    @property
    def bot(self): return Avbot.bot

    @property
    def misc(self): return self.bot.misc

    # Get Timestamp from IBA
    def timestamp(self, t):
        kwargs = dict(microsecond=(t[0]*1000), second=t[1],
            minute=t[2], hour=t[3], day=t[4], month=t[5], year=t[6])
        timestamp = self.misc.datetime.datetime(**kwargs)
        return timestamp

# Instance Class
pda = PDA()