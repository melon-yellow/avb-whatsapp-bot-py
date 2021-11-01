
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
import os
import py_misc
import requests
from py_wapp import Bot

# Modules
from . import iba
from . import pims
from . import torque
from . import trefila
from . import laminador

##########################################################################################################################

# Create Instance of Bot
avbot = Bot({
    'addr': os.getenv('WHATSAPP_TARGET_ADDR'),
    'auth':{
        'user': os.getenv('WHATSAPP_TARGET_USER'),
        'password': os.getenv('WHATSAPP_TARGET_PASSWORD')
    }
})

##########################################################################################################################

# Set API Port
avbot.port(1516)

# Set Authentication
for i in range(os.getenv('WHATSAPP_USERS')):
    avbot.user(os.getenv(f'WHATSAPP_USER_${i + 1}'))
    avbot.password(os.getenv(f'WHATSAPP_PASSWORD_${i + 1}'))

##########################################################################################################################

# Create Connection
makesql = (lambda db: py_misc.MySQL(
    host = 'localhost',
    port = os.getenv('MYSQL_PORT'),
    user = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASSWORD'),
    database = db
))

##########################################################################################################################

# Set Avbot SQL Connection
avbot.sqlconn(makesql('bot'))

##########################################################################################################################

# Load Actions
laminador.__load__(avbot)
trefila.__load__(avbot, makesql('lam'))

##########################################################################################################################

@py_misc.schedule.each.one.minute.do
def one_minute_scheudule():
    pims.check.cimios(avbot)

##########################################################################################################################

@py_misc.schedule.each.one.hour.do.at('00:00')
def one_hour_scheudule():
    requests.get('http://localhost:8085/misc/one_hour_schedule.php')
    torque.off.send(avbot)
    # Avbot.send('grupo_trefila', Lam.frio.prod(), 'schedule::lam.frio.prod(grupo_trefila)')
    # Avbot.send('calegari', Lam.quente.prod(), 'schedule::lam.quente.prod(calegari)')

##########################################################################################################################

# Start Avbot
avbot.start()

##########################################################################################################################

# Wait 3 seconds
py_misc.time.sleep(3)
# Send Message
sent = avbot.send('anthony', 'Python Avbot Started!', 'py_warning')
@sent.on.reply
def abc123(message):
    sent2 = message.quote('Got It!', 'got_reply')
    @sent2.on.reply
    def xyz789(message):
        sent3 = message.quote('Am i one of the Dummies?', 'not_so_dummy?')
        @sent3.on.reply
        def yfw234(message):
            # On Affirmative
            if avbot.chat.yes(message):
                sent4 = message.quote(':(', 'avbot_is_sad')
            # On Negative
            elif avbot.chat.no(message):
                sent4 = message.quote(':)', 'avbot_is_happy')
            # On Neither
            else: # Get Error Understanding
                sentL = message.quote(':|', 'avbot_is_confused')
                sentL.reply(yfw234)

##########################################################################################################################

# Check PIMS Cim-IOs
pims.check.cimios(avbot)

##########################################################################################################################

# Keep Main Thread Alive
avbot.keepalive()

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
