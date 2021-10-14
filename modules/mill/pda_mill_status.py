import sys
import json
import requests
import py_misc

# Import Message Class
from ..core import Whapp
whapp = Whapp(py_misc, target)

# Get Input Params
target = json.load(open('F:/pda/avbot/core/target.json', 'r'))
status = str(sys.argv[1])
data = json.loads(str(sys.argv[2]))

message = Message(target['addr'], target['auth'])

try: # Request
    res = requests.post(
        target['addr'],
        target['auth'],
        json = dict(
            action='pda_mill_status',
            status=str(args[1]),
            data=json.loads(str(args[2]))
        )
    )
    res = print(json.loads(res.text))
except: # If Server Not Responding
    res = print(dict(status='Connection Error'))

# Status do Laminador
@Avbot.add('pda_mill_status')
def pda_mill_status(req):
    # Check Request
    if not Avbot.check(req, 'status', str): raise Exception('key "status" not found')
    if not Avbot.check(req, 'data', dict): raise Exception('key "data" not found')
    status = req['status']
    data = req['data']

    # Options Dictionary
    switcher = dict(
        ghost = 'Passando barra fantasma!',
        exit_fur = 'Peça saindo do forno!',
        start = 'Laminador produzindo! 🙏',
        stop = 'Laminador parado! 🤷‍♂️💸‍',
        gap = 'Laminador no GAP‍! 🙏💰',
        gap_off = 'O GAP foi desligado! 🤷‍♂️🐢',
        cobble = 'Sucata no laminador! 🤦💸💸‍'
    )

    # Check Status Key
    if status not in switcher: return False

    # Get Message Text
    log = 'api::pda_mill_status({})'.format(status)
    msg = switcher[status]

    # Get Cause
    if status == 'cobble' or status == 'gap_off':
        cause = get_cause(data, status)
        if isinstance(cause, str) and cause != '':
            msg = (msg + '\n' + '_Motivo: ' + cause + '_')
        # Dump Json
        Avbot.misc.json.dump(req, open('pda_mill_status.json', 'w'))

    # Send Messages
    Avbot.bot.send('grupo_supervisores', msg, log)

    # Send only Start/Stop Messages
    if status != 'ghost' and status != 'exit_fur':
        Avbot.bot.send('gerencia_laminacao', msg, log)

    # Send Message with Cause
    Avbot.bot.send('anthony', msg, log)