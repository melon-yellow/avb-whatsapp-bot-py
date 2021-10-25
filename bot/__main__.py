
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

# Imports
import requests
from py_wapp import Bot

# Modules
from . import iba
from . import pims
from . import torque
from . import trefila

##########################################################################################################################

# Create Instance of Bot
Avbot = Bot({
    'addr':'http://localhost:1615/bot',
    'auth':{
        'user':'gusal2.avb.whatsapp',
        'password':'n2u95n345bu345u34sdsnujdisj3w3wq3ng32'
    }
})

# Set Authentication
Avbot.port(1516).user('gusal2.avb.whatsapp').password(
    'vet89u43t0jw234erwedf21sd9R78fe2n2084u'
)

##########################################################################################################################

# Create Connection
makesql = (lambda db: Avbot.misc.MySQL(
    host = 'localhost',
    port = '1517',
    user = 'root',
    password = 'vet89u43t0jw234erwedf21sd9R78fe2n2084u',
    database = db
))

##########################################################################################################################

# Set Avbot SQL Connection
Avbot.sqlconn(makesql('bot'))

##########################################################################################################################

# Load Actions from Trefila
trefila.__load__(Avbot, makesql('lam'))

##########################################################################################################################

@Avbot.misc.schedule.each.one.minute.do
def one_minute_scheudule():
    pims.check.cimios(Avbot)

##########################################################################################################################

@Avbot.misc.schedule.each.one.hour.do.at('00:00')
def one_hour_scheudule():
    torque.off.send(Avbot)
    requests.get('http://localhost:8085/misc/one_hour_schedule.php')
    # Avbot.send('grupo_trefila', Lam.frio.prod(), 'schedule::lam.frio.prod(grupo_trefila)')
    # Avbot.send('calegari', Lam.quente.prod(), 'schedule::lam.quente.prod(calegari)')

##########################################################################################################################

# Start Avbot
Avbot.start()

##########################################################################################################################

# Wait 3 seconds
Avbot.misc.time.sleep(3)
# Send Message
sent = Avbot.send('anthony', 'Python Avbot Started!', 'py_warning')
@sent.reply
def abc123(message):
    sent2 = message.quote('Got It!', 'got_reply')
    @sent2.reply
    def xyz789(message):
        sent3 = message.quote('Am i one of the Dummies?', 'not_so_dummy?')
        @sent3.reply
        def yfw234(message):
            # On Affirmative
            if Avbot.chat.yes(message):
                sent4 = message.quote(':(', 'avbot_is_sad')
            # On Negative
            elif Avbot.chat.no(message):
                sent4 = message.quote(':)', 'avbot_is_happy')
            # On Neither
            else: # Get Error Understanding
                sentL = message.quote(':|', 'avbot_is_confused')
                sentL.reply(yfw234)

##########################################################################################################################

# Check PIMS Cim-IOs
pims.check.cimios(Avbot)

##########################################################################################################################

# Keep Main Thread Alive
Avbot.keepalive()

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
