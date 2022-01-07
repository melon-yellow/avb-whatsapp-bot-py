
##########################################################################################################################
#                                                       PY-AVBOT                                                         #
##########################################################################################################################
#                                                                                                                        #
#                                                 Whatsapp Bot for AVB                                                   #
#                                          Multi-language API for Whatsapp Bot                                           #
#                             ---------------- Python3 -- NodeJS -- MySQL ----------------                               #
#                                                * Under Development *                                                   #
#                                  https://github.com/melon-yellow/avb-whatsapp-bot-py                                  #
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
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Create Instance of Bot
avbot = Bot({
    'address': os.getenv('WHATSAPP_TARGET_ADDRESS'),
    'user': os.getenv('WHATSAPP_TARGET_USER'),
    'password': os.getenv('WHATSAPP_TARGET_PASSWORD')
})

##########################################################################################################################

# Set Network API
app = py_misc.Express(log=False)

# Set Network Endnode
avbot.network.route(
    route='whatsapp',
    app=app
)

# Set Network API Port
app.port(
    int(os.getenv('WHATSAPP_PORT'))
)

# Set Network Authentication
for i in range(
    int(os.getenv('WHATSAPP_USERS'))
):
    avbot.network.users.update({
        os.getenv(f'WHATSAPP_USER_${i + 1}'):
        os.getenv(f'WHATSAPP_PASSWORD_${i + 1}')
    })

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Create SQL Connection
def makesql(db: str):
    return py_misc.MySQL(
        host = 'localhost',
        port = os.getenv('MYSQL_PORT'),
        user = os.getenv('MYSQL_USER'),
        password = os.getenv('MYSQL_PASSWORD'),
        database = db
    )

##########################################################################################################################

# Set Avbot SQL Connection
avbot.sqlconn(makesql('bot'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Load Actions
laminador.__load__(avbot)
trefila.__load__(avbot, makesql('lam'))

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# One Minute Schedule
@py_misc.schedule.each.one.minute.do
def one_minute_scheudule():
    pims.check.cimios(avbot)

# One Hour Schedule
@py_misc.schedule.each.one.hour.do.at('00:00')
def one_hour_scheudule():
    requests.get('http://localhost:8085/misc/one_hour_schedule.php')
    torque.off.send(avbot)
    # Avbot.send(to='grupo_trefila', text=lam.frio.prod(), log='schedule::lam.frio.prod(grupo_trefila)')
    # Avbot.send(to='calegari', text=lam.quente.prod(), log='schedule::lam.quente.prod(calegari)')

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Start Bot
avbot.start()

# Start Network API
app.start()

##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################

# Wait 3 seconds
py_misc.time.sleep(3)
# Send Message
sent = avbot.send(to='anthony', text='Python Avbot Started!', log='py_warning')
@sent.on.reply
def abc123(message: Bot.Message):
    sent2 = message.quote(text='Got It!', log='got_reply')
    @sent2.on.reply
    def xyz789(message: Bot.Message):
        sent3 = message.quote(text='Am i one of the Dummies?', log='not_so_dummy?')
        @sent3.on.reply
        def yfw234(message: Bot.Message):
            # On Affirmative
            if avbot.chat.yes(message):
                sent4 = message.quote(text=':(', log='avbot_is_sad')
            # On Negative
            elif avbot.chat.no(message):
                sent4 = message.quote(text=':)', log='avbot_is_happy')
            # On Neither
            else: # Get Error Understanding
                sentL = message.quote(text=':|', log='avbot_is_confused')
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
