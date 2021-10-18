
##########################################################################################################################
#                                                       PY-AVBOT-61                                                      #
##########################################################################################################################
#                                                                                                                        #
#                                                 Whatsapp Bot for AVB                                                   #
#                                          Multi-language API for Whatsapp Bot                                           #
#                             ---------------- Python3 -- NodeJS -- MySQL ----------------                               #
#                                                * Under Development *                                                   #
#                                    https://github.com/anthony-freitas/py-avbot-61                                      #
#                                                                                                                        #
##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Import Whatsapp Bot
from py_wapp import Bot

##########################################################################################################################
#                                                    INSTANCE WAPP BOT                                                   #
##########################################################################################################################

# Create Instance of Bot
Avbot = Bot({
    'addr':'http://localhost:1615/bot',
    'auth':{
        'user':'avb.whatsapp',
        'password':'ert2tyt3tQ3423rubu99ibasid8hya8da76sd'
    }
})

# Set Authentication
Avbot.port(1516).user('avb.whatsapp').password(
    'vet89u43t0jw234erwedf21sd9R78fe2n2084u'
)

##########################################################################################################################
#                                                       SQL CONNECT                                                      #
##########################################################################################################################

# Create Connection
def MySQL(database):
    return Avbot.misc.mysql(
        host = 'localhost', port = '1517', user = 'root',
        password = 'vet89u43t0jw234erwedf21sd9R78fe2n2084u',
        database = database
    )

# Instance Objects
bot_db = MySQL('bot')
lam_db = MySQL('lam')
iba_db = MySQL('pda')

# Set Avbot SQL Connection
Avbot.bot.sqlconn(bot_db)

# Instance Object
stopTref = ParadasTrefila()

##########################################################################################################################
#                                                   ONE MINUTE SCHEDULE                                                  #
##########################################################################################################################

@Avbot.misc.schedule.each.one.minute.do
def one_minute_scheudule():
    py_mes_check_cimios()

##########################################################################################################################
#                                                    ONE HOUR SCHEDULE                                                   #
##########################################################################################################################

@Avbot.misc.schedule.each.one.hour.do.at('00:00')
def one_hour_scheudule():
    Avbot.bot.misc.requests.get('http://localhost:8085/misc/one_hour_schedule.php')
    # Avbot.bot.send('grupo_trefila', Lam.frio.prod(), 'schedule::lam.frio.prod(grupo_trefila)')
    # Avbot.bot.send('calegari', Lam.quente.prod(), 'schedule::lam.quente.prod(calegari)')
    torqueOff.send_off()

##########################################################################################################################
#                                                           TESTING                                                      #
##########################################################################################################################

# Test Function
@Avbot.misc.call.safe
def avbot_start_chat():
    # Wait 3 seconds
    Avbot.bot.misc.time.sleep(3)
    # Send Message
    sent = Avbot.bot.send('anthony', 'Python Avbot Started!', 'py_warning')
    @sent.reply
    def abc123(message):
        sent2 = message.quote('Got It!', 'got_reply')
        @sent2.reply
        def xyz789(message):
            sent3 = message.quote('Am i one of the Dummies?', 'not_so_dummy?')
            @sent3.reply
            def yfw234(message):
                # On Affirmative
                if Avbot.bot.chat.yes(message):
                    sent4 = message.quote(':(', 'avbot_is_sad')
                # On Negative
                elif Avbot.bot.chat.no(message):
                    sent4 = message.quote(':)', 'avbot_is_happy')
                # On Neither
                else: # Get Error Understanding
                    sentL = message.quote(':|', 'avbot_is_confused')
                    sentL.reply(yfw234)

##########################################################################################################################
#                                                        KEEP ALIVE                                                      #
##########################################################################################################################

# If Executed as Main
if __name__ == '__main__':

    # Start Avbot
    Avbot.start()
    
    # Send Python Avbot Started
    avbot_start_chat()
    
    # Check PIMS Cim-IOs
    Avbot.misc.call.safe(
        py_mes_check_cimios
    )()
    
    # Keep Alive
    Avbot.keepalive()

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
