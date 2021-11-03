
##########################################################################################################################

# Imports
import datetime
from py_misc import MySQL
from py_wapp import Bot

# Modules
from . import turno

##########################################################################################################################

# Get Last Stop
def get_last(db: MySQL, mq: int):
    # Create Query
    query = ' '.join(
        ('SELECT * FROM lam_frio_interr_turno',
        'WHERE timestamp = (SELECT MAX(timestamp)',
        f'FROM lam_frio_interr_turno WHERE mq = {mq})')
    )
    # Execute Query
    last = db.get(query)
    last = None if len(last) == 0 else last[0]
    return last

##########################################################################################################################

# Get Difference of Time
def difference(last: list, now: datetime.datetime):
    dif = dict(stop=None, tempo_parado=None, stop_id=None)
    if last != None and not last[4]:
        dif['tempo_parado'] = abs((now - last[0]).seconds)
        dif['stop_id'] = last[7]
        dif['stop'] = last[0]
    return dif

##########################################################################################################################

# Get Difference
def assemble(mq: int, starting: bool):
    last = get_last(mq)
    stop_time = turno.timestamp
    stop_date = last[1] if last != None else turno.timestamp.date()
    stop_turno = last[2] if last != None else turno.turno()
    if not starting:
        stop_time -= datetime.timedelta(minutes=5)
        stop_date = turno.timestamp.date()
        stop_turno = turno.turno()
    # Get time Stopped
    dif = difference(last, stop_time)
    if not starting: dif = dict(stop=None, tempo_parado=None, stop_id=None)
    dat = dict(timestamp=stop_time, date=stop_date,
        turno=stop_turno, mq=mq, starting=starting, stop=dif['stop'],
        tempo_parado=dif['tempo_parado'], stop_id=dif['stop_id'])
    return dat

##########################################################################################################################

# Insert into MySQL
def insert_stop(db: MySQL, dat: dict[str, str], message_id: str):
    # Add Id to Dat
    dat['message_id'] = message_id
    query = ' '.join(
        ('INSERT INTO lam_frio_interr_turno',
        '(`timestamp`, `date`, `turno`, `mq`, `starting`,',
        '`stop`, `tempo_parado`, `message_id`, `stop_id`)',
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
    )
    val = (
        dat['timestamp'], dat['date'], dat['turno'], dat['mq'],
        dat['starting'], dat['stop'], dat['tempo_parado'],
        dat['message_id'], dat['stop_id']
    )
    # Execute Query
    inserted = db.execute(query, val)
    return inserted

##########################################################################################################################

# Get Last Stop
def get_stop(db: MySQL, id: str):
    # Create Query
    query = ' '.join(
        ('SELECT * FROM lam_frio_interr_turno',
        f'WHERE (message_id = \'{id}\')')
    )
    # Execute Query
    stop = db.get(query)
    stop = None if len(stop) == 0 else stop[0]
    return stop

##########################################################################################################################

# Get Last Stop
def get_cause(db: MySQL, id: str):
    # Create Query
    query = ' '.join(
        ('SELECT * FROM lam_frio_interr_causa',
        f'WHERE (message_id = \'{id}\')')
    )
    # Execute Query
    cause = db.get(query)
    cause = None if len(cause) == 0 else cause[0]
    return cause

##########################################################################################################################

# Get Last Stop
def get_options(db: MySQL):
    # Create Query
    query = 'SELECT * FROM `interr_causas` ORDER BY `id`'
    # Execute Query
    options = db.get(query)
    return options

##########################################################################################################################

# Get Cause
def insert_cause(db: MySQL, message_id: str, causa: str):
    dat = dict()
    stop = get_stop(message_id)
    if stop == None: return False
    dat['timestamp'] = turno.timestamp
    dat['date'] = stop[1]
    dat['turno'] = stop[2]
    dat['mq'] = stop[3]
    dat['causa'] = causa
    dat['message_id'] = message_id
    query = ' '.join(('INSERT INTO lam_frio_interr_causa',
        '(`timestamp`, `date`, `turno`, `mq`, `causa`, `message_id`)',
        'VALUES (%s, %s, %s, %s, %s, %s)'))
    val = (dat['timestamp'], dat['date'], dat['turno'],
        dat['mq'], dat['causa'], dat['message_id'])
    # Execute Query
    inserted = db.execute(query, val)
    return inserted

##########################################################################################################################

# Get Cause
def insert_sent_options(db: MySQL, message_id: str, quote: bool = False):
    dat = dict()
    dat['timestamp'] = turno.timestamp
    dat['sent'] = 'lam_frio_interr_options'
    dat['sent'] += '_quote' if quote else ''
    dat['id'] = message_id
    query = ' '.join(('INSERT INTO sent_misc',
        '(`timestamp`, `sent`, `id`) VALUES (%s, %s, %s)'))
    val = (dat['timestamp'], dat['sent'], dat['id'])
    # Execute Query
    inserted = db.execute(query, val)
    return inserted

##########################################################################################################################

# Get Last Stop
def get_last_sent_options(db: MySQL, quote: bool = False):
    # Create Query
    cond = 'OR sent = \'lam_frio_interr_options_quote\'' if quote else ''
    query = ' '.join(
        ('SELECT * FROM sent_misc WHERE timestamp =',
        '(SELECT MAX(timestamp) FROM sent_misc',
        f'WHERE sent = \'lam_frio_interr_options\' {cond})')
    )
    # Execute Query
    last = db.get(query)
    last = None if len(last) == 0 else last[0]
    return last

##########################################################################################################################

# Send Message with Options
def send_options(bot: Bot, to: str):
    # Get Stop Cause Options
    op = get_options()
    # Generate List Message
    msg_op = 'Escolha uma ou mais das opções abaixo:\n\n'
    for item in op:
        no = str(item[0])
        no = '0' + no if len(no) == 1 else no
        msg_op += no + ' - '
        msg_op += str(item[1]) + '\n'
    # Send Options
    sent = bot.send(to=to, text=msg_op, log='trf_stop_options')
    # Insert on MySQL
    e = insert_sent_options(sent.id)
    return sent

##########################################################################################################################

# Send Message with Options
def quote_options(bot: Bot, to: str, id: str):
    # Generate Message
    msg = 'Aqui estão as opções!'
    # Send Options
    sent = bot.send(to=to, text=msg, log='quote_options', quote=id)
    # Insert on MySQL
    e = insert_sent_options(sent.id, True)
    return sent

##########################################################################################################################

# Send Message with Options
def show_options(bot: Bot, to: str):
    # Get Last Stop Options
    lts = get_last_sent_options()
    mn3 = turno.timestamp - datetime.timedelta(days=3)
    if lts == None:
        send_options(bot, to)
        lts = get_last_sent_options()
    elif lts == None: return None
    elif lts[0] <= mn3:
        send_options(bot, to)
        lts = get_last_sent_options()
    elif lts == None: return None
    return lts[2]
    
##########################################################################################################################
