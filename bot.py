
##########################################################################################################################
#                                                        AVBOT                                                           #
##########################################################################################################################
#                                                                                                                        #
#                                                     Avbot v1.6.4                                                       #
#                                          Multi-language API for Whatsapp Bot                                           #
#                             ---------------- Python3 -- NodeJS -- MySQL ----------------                               #
#                                             This is a Development Server                                               #
#                                                 Powered by venom-bot                                                   #
#                                                                                                                        #
##########################################################################################################################
#                                                      MAIN CODE                                                         #
##########################################################################################################################

# Imports
import core

# Create Instance of Bot
Avbot = core.Bot()

##########################################################################################################################
#                                                       SQL CONNECT                                                      #
##########################################################################################################################

# Create Connection
def MySQL(database):
    return Avbot.bot.misc.mysql(
        host = '127.0.0.1', port = '1517', user = Avbot.sql.user,
        password = Avbot.sql.password, database = database)

# Instance Object
lam_db = MySQL('lam')
iba_db = MySQL('pda')

##########################################################################################################################
#                                                    CLASSE LAMINADOR                                                    #
##########################################################################################################################

# Laminador Class
class Laminador:

    def __init__(self):
        # General Methods for Lam
        class Gen:

            def __init__(self):
                # Allow info inside Turno
                self.misc = Avbot.misc

            # Relatorio Producao
            def prod(self):
                return None

            # Relatorio Producao do Mes
            def prod_mes(self):
                return None

            # Relatorio Turno
            def turno(self):
                return None

        self.quente = Gen()
        self.frio = Gen()

# Instance Class
Lam = Laminador()

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

##########################################################################################################################
#                                                     RELATORIO TURNO                                                    #
##########################################################################################################################

# Turno Class
class Turno:

    # Init Turno
    def __init__(self):
        self.chat = self.Chat()

    # Message Functions
    class Chat:

        @property
        def bot(self): return Avbot.bot

        @property
        def pergunta_parada(self):
            p = ['Alguém pode me dizer o motivo da parada?',
                'Qual o motivo da parada?', 'Por que a máquina parou?',
                'Qual a justificativa da parada?']
            return self.bot.misc.random.choice(p)

        @property
        def obtive_resposta(self):
            p = ['Ok', 'Entendi', 'Certo',
                'Entendido', 'Registrado']
            return self.bot.misc.random.choice(p)

        @property
        def obtive_nao(self):
            p = ['Ok', 'Entendi', 'Certo']
            return self.bot.misc.random.choice(p)

        @property
        def causa_ja_existe(self):
            p = ['Uma informação referente à essa parada ja foi registrada',
                'Já encontrei registros desse horário', 'A causa dessa parada ja foi registrada']
            c = ['deseja substituir esse registro?', 'deseja registrar novamente?',
                'deseja refazer o registro?', 'deseja fazer um novo registro?']
            r = self.bot.misc.random.choice(p) + ', ' + self.bot.misc.random.choice(c)
            return r

    lam_db = lam_db

    @property
    def bot(self): return Avbot.bot

    @property
    def timestamp(self):
        return self.bot.misc.datetime.datetime.now()

    @property
    def turma(self):
        turmas = ['A','B','C','D']
        sel = 0
        return turmas[sel]

    # Get Turno
    def turno(self, ts=None):
        if ts == None: ts = self.timestamp
        y = (lambda t: ts.replace(hour=(t-1), minute=59, second=59, microsecond=999999))
        shift = dict(t0=y(8), t8=y(16), t16=y(24))
        for s in shift:
            if ts <= shift[s]:
                return int(s.replace('t',''))

# Instance Object
turno = Turno()

##########################################################################################################################
#                                                     GET DATA TREFILA                                                   #
##########################################################################################################################

class ParadasTrefila:
    def __init__(self):
        self.turno = turno

    # Get Last Stop
    def get_last(self, mq):
        # Create Query
        query = ' '.join(('SELECT * FROM lam_frio_interr_turno',
            'WHERE timestamp = (SELECT MAX(timestamp)',
            'FROM lam_frio_interr_turno WHERE mq = {})')).format(mq)
        # Execute Query
        last = self.turno.lam_db.get(query)
        last = None if len(last) == 0 else last[0]
        return last


    # Get Difference of Time
    def difference(self, last, now):
        dif = dict(stop=None, tempo_parado=None, stop_id=None)
        if last != None and not last[4]:
            dif['tempo_parado'] = abs((now - last[0]).seconds)
            dif['stop_id'] = last[7]
            dif['stop'] = last[0]
        return dif

    # Get Difference
    def assemble(self, mq, starting):
        last = self.get_last(mq)
        stop_time = self.turno.timestamp
        stop_date = last[1] if last != None else self.turno.timestamp.date()
        stop_turno = last[2] if last != None else self.turno.turno()
        if not starting:
            stop_time -= self.turno.bot.misc.datetime.timedelta(minutes=5)
            stop_date = self.turno.timestamp.date()
            stop_turno = self.turno.turno()
        # Get time Stopped
        dif = self.difference(last, stop_time)
        if not starting: dif = dict(stop=None, tempo_parado=None, stop_id=None)
        dat = dict(timestamp=stop_time, date=stop_date,
            turno=stop_turno, mq=mq, starting=starting, stop=dif['stop'],
            tempo_parado=dif['tempo_parado'], stop_id=dif['stop_id'])
        return dat

    # Insert into MySQL
    def insert_stop(self, dat, message_id):
        # Add Id to Dat
        dat['message_id'] = message_id
        query = ' '.join(('INSERT INTO lam_frio_interr_turno',
            '(`timestamp`, `date`, `turno`, `mq`, `starting`,',
            '`stop`, `tempo_parado`, `message_id`, `stop_id`)',
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'))
        val = (dat['timestamp'], dat['date'], dat['turno'], dat['mq'],
            dat['starting'], dat['stop'], dat['tempo_parado'],
            dat['message_id'], dat['stop_id'])
        # Execute Query
        inserted = self.turno.lam_db.execute(query, val)
        return inserted

    # Get Last Stop
    def get_stop(self, msg_id):
        # Create Query
        query = ' '.join(('SELECT * FROM lam_frio_interr_turno',
            'WHERE (message_id = \'{}\')')).format(msg_id)
        # Execute Query
        stop = self.turno.lam_db.get(query)
        stop = None if len(stop) == 0 else stop[0]
        return stop

    # Get Last Stop
    def get_cause(self, msg_id):
        # Create Query
        query = ' '.join(('SELECT * FROM lam_frio_interr_causa',
            'WHERE (message_id = \'{}\')')).format(msg_id)
        # Execute Query
        cause = self.turno.lam_db.get(query)
        cause = None if len(cause) == 0 else cause[0]
        return cause

    # Get Last Stop
    def get_options(self):
        # Create Query
        query = 'SELECT * FROM `interr_causas` ORDER BY `id`'
        # Execute Query
        options = self.turno.lam_db.get(query)
        return options

    # Get Cause
    def insert_cause(self, message_id, causa):
        dat = dict()
        stop = self.get_stop(message_id)
        if stop == None: return False
        dat['timestamp'] = self.turno.timestamp
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
        inserted = self.turno.lam_db.execute(query, val)
        return inserted

    # Get Cause
    def insert_sent_options(self, message_id, quote=False):
        dat = dict()
        dat['timestamp'] = self.turno.timestamp
        dat['sent'] = 'lam_frio_interr_options'
        dat['sent'] += '_quote' if quote else ''
        dat['id'] = message_id
        query = ' '.join(('INSERT INTO sent_misc',
            '(`timestamp`, `sent`, `id`) VALUES (%s, %s, %s)'))
        val = (dat['timestamp'], dat['sent'], dat['id'])
        # Execute Query
        inserted = self.turno.lam_db.execute(query, val)
        return inserted

    # Get Last Stop
    def get_last_sent_options(self, quote=False):
        # Create Query
        cond = 'OR sent = \'lam_frio_interr_options_quote\'' if quote else ''
        query = ' '.join(('SELECT * FROM sent_misc',
            'WHERE timestamp = (SELECT MAX(timestamp) FROM sent_misc',
            'WHERE sent = \'lam_frio_interr_options\' {})')).format(cond)
        # Execute Query
        last = self.turno.lam_db.get(query)
        last = None if len(last) == 0 else last[0]
        return last

    # Send Message with Options
    def send_options(self, to):
        # Get Stop Cause Options
        op = self.get_options()
        #Generate List Message
        msg_op = 'Escolha uma ou mais das opções abaixo:\n\n'
        for item in op:
            no = str(item[0])
            no = '0' + no if len(no) == 1 else no
            msg_op += no + ' - '
            msg_op += str(item[1]) + '\n'
        # Send Options
        sent = Avbot.bot.send(to, msg_op, 'trf_stop_options')
        # Insert on MySQL
        e = self.insert_sent_options(sent.id)
        return sent

    # Send Message with Options
    def quote_options(self, to, sent_id):
        #Generate Message
        msg = 'Aqui estão as opções!'
        # Send Options
        sent = Avbot.bot.send(to, msg, 'quote_options', sent_id)
        # Insert on MySQL
        e = self.insert_sent_options(sent.id, True)
        return sent

    # Send Message with Options
    def show_options(self, to):
        # Get Last Stop Options
        lts = self.get_last_sent_options()
        mn3 = self.turno.timestamp - self.turno.bot.misc.datetime.timedelta(days=3)
        if lts == None:
            self.send_options(to)
            lts = self.get_last_sent_options()
        elif lts == None: return None
        elif lts[0] <= mn3:
            self.send_options(to)
            lts = self.get_last_sent_options()
        elif lts == None: return None
        return lts[2]

    # Close Connection
    def close(self):
        self = None

# Instance Object
stopTref = ParadasTrefila()

##########################################################################################################################
#                                                    PDA MILL STATUS                                                     #
##########################################################################################################################

# Status do Laminador
@Avbot.add('pda_mill_status')
def pda_mill_status(req):
    if not Avbot.check(req, 'status', str): return False
    status = req['status']
    # Options Dictionary
    switcher = dict(
        gap = 'Laminador no GAP‍! 🙏💰',
        stop = 'Laminador parado! 🤷‍♂️💸‍',
        start = 'Laminador produzindo! 🙏',
        cobble = 'Sucata no laminador! 🤦💸💸‍',
        gap_off = 'O GAP foi desligado! 🤷‍♂️🐢'
    )
    if status not in switcher: return False
    log = 'api::pda_mill_status({})'.format(status)
    msg = switcher[status]
    # Send Message
    Avbot.bot.send('gerencia_laminacao', msg, log)
    Avbot.bot.send('anthony', msg, log)

##########################################################################################################################
#                                                   PDA TREFILA STATUS                                                   #
##########################################################################################################################

# Status da Trefila
@Avbot.add('pda_trf_status')
def pda_trf_status(req):
    if not Avbot.check(req, 'mq', str): return False
    if not Avbot.check(req, 'status', str): return False
    mq = req['mq']
    status = req['status']
    # Options Dictionary
    switcher = dict(
        stop = '😔 Máquina {} parada!‍',
        start = '😁 Máquina {} ligada!'
    )
    if status not in switcher: return False
    log = 'api::pda_trf_status({}, {})'.format(mq, status)
    msg = switcher[status].format(mq)

    # Assemble Data
    starting = (status == 'start')
    dat = stopTref.assemble(mq, starting)

    # If Starting
    if starting:
        # Send Options Message
        if dat['stop'] != None:
            sec = dat['tempo_parado']
            d = Avbot.misc.datetime.timedelta(seconds=sec)
            parada = Avbot.bot.chat.timedelta(d)
            msg += '\n⏱️ {} de parada.'.format(parada)
        # Quest Group
        gmsg = Avbot.bot.misc.copy.deepcopy(msg)
        gmsg += '\n🗒️ {}'.format(stopTref.turno.chat.pergunta_parada)
        gmsg += ' Escolha entre as opções da lista.'
        quote = stopTref.show_options('grupo_trefila')
        # Send Message
        Avbot.bot.send('anthony', msg, log)
        Avbot.bot.send('jayron', msg, log)
        sent = Avbot.bot.send('grupo_trefila', gmsg, log, quote)
    else: # If Not Starting
        Avbot.bot.send('anthony', msg, log)
        sent = Avbot.bot.send('jayron', msg, log)

    # Insert to MySQL
    e = stopTref.insert_stop(dat, sent.id)

    # On Reply
    @sent.reply
    def add_cause(message):

        # On Ambiguous Message
        def ambiguous_msg(msg, has_float=False):
            if has_float:
                ambig = ('Sua mensagem não foi muito clara, ' +
                'evite o uso de pontos ou vírgulas e não digite nenhum ' +
                'número que não indique diretamente a causa da parada.')
            else:
                ambig = ('Se estiver tentando registrar a causa da ' +
                'parada de uma máquina, digite um número que esteja na lista. ' +
                'Se houver mais de uma causa, separe os números com Espaço.')
            # Send Message
            log = 'sent_ambiguous_message'
            sent_ambig = Avbot.bot.send('anthony', ambig, log, msg.id)
            sent_ambig.reply(add_cause)
            return False

        # Verify Cause
        def verify_causas(msg):
            strin = Avbot.bot.chat.clean(msg.body)
            char = Avbot.bot.misc.re.findall('[a-zA-Z0-9]+', strin)
            num = Avbot.bot.misc.re.findall('[0-9]+', strin)
            floats = Avbot.bot.misc.re.findall('\d+\.\d+', strin)
            floats += Avbot.bot.misc.re.findall('\d+\,\d+', strin)
            if len(char) == 0: return False
            if len(num) == 0: return ambiguous_msg(msg)
            if len(floats) > 0: return ambiguous_msg(msg, True)
            strin = Avbot.bot.misc.re.sub('[^0-9]', ' ', strin)
            strin = Avbot.bot.chat.clean(strin)
            causas = strin.split(' ')
            for i in range(len(causas)):
                causas[i] = int(causas[i].lstrip('0'))
            return causas

        # Check for Existing Cause
        __cause__ = stopTref.get_cause(sent.id)

        # If Cause does not Exist
        if __cause__ == None:
            causas = verify_causas(message)
            if causas == False: return False
            causas_json = Avbot.bot.misc.json.dumps(causas)
            stopTref.insert_cause(sent.id, causas_json)

        else: # If cause already Exists
            msg = stopTref.turno.chat.causa_ja_existe
            sent2 = message.quote(msg, 'trf_status_got_existing')
            # On Reply
            @sent2.reply
            def new_cause(confirm):
                # On Affirmative
                if Avbot.bot.chat.yes(confirm):
                    stopTref.insert_cause(sent.id, message.body)
                    sent2.reply(lambda: None)
                # On Negative
                elif Avbot.bot.chat.no(confirm):
                    sent2.reply(lambda: None)
                # On Neither
                else: # Get Error Understanding
                    error = Avbot.bot.chat.error.understand
                    sentL = confirm.quote(error, 'trf_status_didnt_got_it')
                    sentL.reply(new_cause)

##########################################################################################################################
#                                                    REPORT TREFILA TURNO                                                #
##########################################################################################################################

# Relaatorio Turno Trefila
@Avbot.add('pda_trf_report')
def pda_trf_report(req):
    if not Avbot.check(req, 't', list): return False
    if not Avbot.check(req, 'util', list): return False
    t_pda = pda.timestamp(req['t'])
    util = req['util']

    # Get Shift and Date
    d = t_pda.date()
    t = t_pda.hour
    turma = stopTref.turno.turma

    # Fix Shift
    if 7 <= t and t <= 9: t = 0
    elif 15 <= t and t <= 17: t = 8
    elif 23 <= t or t <= 1: t = 16
    else: return False

    # Fix Date
    if t == 16:
        d -= Avbot.bot.misc.datetime.timedelta(days=1)

    # Create Query
    def qur(tb):
        return ' '.join(('SELECT * FROM `{}` WHERE (`turno` = {}',
            'AND `date` = \'{}\') ORDER BY `timestamp`')).format(tb, t, d)
    # Get queries
    query1 = qur('lam_frio_interr_turno')
    query2 = qur('lam_frio_interr_causa')

    # Execute Query
    paradas = stopTref.turno.lam_db.get(query1)
    causas = stopTref.turno.lam_db.get(query2)

    # Check for Registers
    if len(paradas) == 0: return False
    temp = list()

    # Find Start
    def find_start(stop):
        for start in paradas:
            if stop[0] == start[5]:
                return list(start)
        return None

    # Find Causa
    def find_causa(ids):
        for causa in causas:
            if (causa[5] in ids):
                return causa[4]
        return None

    # Main Loop
    for stop in paradas:
        stop = list(stop)
        if not stop[4]:
            start = find_start(stop)
            if start != None:
                causa = find_causa([start[7], start[8]])
                start.append(causa)
                temp.append(start)
            else:
                causa = find_causa([stop[7]])
                stop.append(causa)
                temp.append(stop)

    # Assign Values
    paradas = Avbot.bot.misc.copy.deepcopy(temp)
    temp = [list(),list(),list(),list(),list()]

    # Filter by Machine
    for item in paradas: temp[item[3]-1].append(item)
    paradas = Avbot.bot.misc.copy.deepcopy(temp)

    def get_cause(item):
        if item[7] == None: item[7] = 'NULL'
        if item[8] == None: item[8] = 'NULL'
        # Create Query
        query = ' '.join(('SELECT * FROM `lam_frio_interr_causa`',
            'WHERE (message_id = \'{}\' OR message_id = \'{}\')',
            'ORDER BY `timestamp` DESC')).format(item[7], item[8])
        # Execute Query
        cause = stopTref.turno.lam_db.get(query)
        cause = list() if len(cause) == 0 else cause[0]
        if len(cause) > 0: cause = Avbot.bot.misc.json.loads(cause[4])
        return cause

    def format_cause(item):
        ca = get_cause(item)
        if len(ca) == 0: return 'causa não declarada'
        cause = ''
        op = stopTref.get_options()
        op[0][1] = 'causa não listada'
        for c in range(len(ca)):
            sep = ('' if c == 0 else (' e ' if (c == len(ca) - 1) else ', '))
            for o in range(len(op)):
                if ca[c] != op[o][0]: continue
                thisc = sep + op[o][1]
            cause += thisc.lower()
        return cause

    # Create Message
    def turn(h):
        return '{}{}:00'.format('0' if len(str(h)) < 2 else '', h)

    # Title
    msg = ('\n' +
        '------------------------------------------------------\n' +
        '🤖 *Relatório de Paradas Trefila* 👾\n' +
        '------------------------------------------------------\n' +
        '📋 *Produção dia {}*\n'.format(d.strftime('%d/%m/%Y')) +
        '🕒 *Turno das {} às {}*\n'.format(turn(t), turn(t+8)) +
        '------------------------------------------------------')
        #'🔠 *Turma {}*\n'.format(turma) +

    # Machine Stops
    for maquina in paradas:
        mq = 1 + paradas.index(maquina)
        mq = '\n*Máquina {}:*'.format(mq)
        mq += '\n------------------------------------------------------'
        msg += mq if len(maquina) > 0 else ''
        Avbot.bot.misc.datetime.timedelta(seconds=0)
        for item in maquina:
            msg += '\n⚠️ Parada de '
            if item[6] == None: msg += 'duração indeterminada'
            else:
                delt = Avbot.bot.misc.datetime.timedelta(seconds=item[6])
                msg += Avbot.bot.chat.timedelta(delt)
            msg += ' por '
            msg += format_cause(item)
        sep = '\n------------------------------------------------------'
        msg += sep if len(maquina) > 0 else ''

    # Insert Turno Util
    def insert_util_turno(mq):
        query = ' '.join(('INSERT INTO `lam_frio_util`',
            '(`timestamp`, `date`, `turno`, `mq`, `sec`, `util`)',
            'VALUES (%s, %s, %s, %s, %s, %s)'))
        val = (t_pda, d, t, mq, util[0], util[mq])
        stopTref.turno.lam_db.execute(query, val)
    # Iterate over Util
    for i in range(5):
        insert_util_turno(i+1)

    # Set conditons to Util
    send_util = True

    # Get Turno Util
    def get_util_turno():
        query_last_turno = ' '.join(('SELECT * FROM `lam_frio_util`',
            'WHERE (`turno` = {} AND `date` = \'{}\')',
            'ORDER BY `mq`')).format(t-8, d)
        last_turno = stopTref.turno.lam_db.get(query_last_turno)
        # Check for Data
        if len(last_turno) < 1: send_util = False
        # Iterate over Util
        def get_mq(mq):
            for row in last_turno:
                if row[3] == mq:
                    util[mq] -= row[5]
                    return True
        # Iterate over Data
        util[0] = 28800
        for i in range(5): get_mq(i+1)
    # If Turno > 0
    if t > 0: get_util_turno()

    # Format Util
    ut = dict()
    # Calc Util
    ut['u1'] = ((util[1] / util[0]) * 100)
    ut['u2'] = ((util[2] / util[0]) * 100)
    ut['u3'] = ((util[3] / util[0]) * 100)
    ut['u4'] = ((util[4] / util[0]) * 100)
    ut['u5'] = ((util[5] / util[0]) * 100)
    ut['u'] = ((ut['u2'] + ut['u3'] + ut['u4'] + ut['u5']) / 4)
    # Fix Util
    ut['u1'] = str(round(ut['u1'], 2))
    ut['u2'] = str(round(ut['u2'], 2))
    ut['u3'] = str(round(ut['u3'], 2))
    ut['u4'] = str(round(ut['u4'], 2))
    ut['u5'] = str(round(ut['u5'], 2))
    ut['u'] = str(round(ut['u'], 2))
    # Calc Time
    ut['t1'] = Avbot.bot.misc.datetime.timedelta(seconds=(util[0] - util[1]))
    ut['t2'] = Avbot.bot.misc.datetime.timedelta(seconds=(util[0] - util[2]))
    ut['t3'] = Avbot.bot.misc.datetime.timedelta(seconds=(util[0] - util[3]))
    ut['t4'] = Avbot.bot.misc.datetime.timedelta(seconds=(util[0] - util[4]))
    ut['t5'] = Avbot.bot.misc.datetime.timedelta(seconds=(util[0] - util[5]))
    ut['t'] = (ut['t2'] + ut['t3'] + ut['t4'] + ut['t5'])
    # Fix Time
    ut['t1'] = Avbot.bot.chat.timedelta(ut['t1'])
    ut['t2'] = Avbot.bot.chat.timedelta(ut['t2'])
    ut['t3'] = Avbot.bot.chat.timedelta(ut['t3'])
    ut['t4'] = Avbot.bot.chat.timedelta(ut['t4'])
    ut['t5'] = Avbot.bot.chat.timedelta(ut['t5'])
    ut['t'] = Avbot.bot.chat.timedelta(ut['t'])

    # Append Util
    ut_msg = ('\n' +
        '*Utilização:*\n' +
        '------------------------------------------------------\n' +
        '📊 Utilização M2 (Turno): {}%\n'.format(ut['u2']) +
        '📊 Utilização M3 (Turno): {}%\n'.format(ut['u3']) +
        '📊 Utilização M4 (Turno): {}%\n'.format(ut['u4']) +
        '📊 Utilização M5 (Turno): {}%\n'.format(ut['u5']) +
        '📊 *Utilização Global: {}%*\n'.format(ut['u']) +
        '------------------------------------------------------\n' +
        '*Tempo Parado:*\n' +
        '------------------------------------------------------\n' +
        '⚠️ Tempo parado M2 (Turno):\n{}\n'.format(ut['t2']) +
        '⚠️ Tempo parado M3 (Turno):\n{}\n'.format(ut['t3']) +
        '⚠️ Tempo parado M4 (Turno):\n{}\n'.format(ut['t4']) +
        '⚠️ Tempo parado M5 (Turno):\n{}\n'.format(ut['t5']) +
        '⚠️ *Paradas Totais no Turno:*\n*{}*\n'.format(ut['t']) +
        '------------------------------------------------------')
    # Check for Conditions to Append
    if send_util: msg += ut_msg
    msg += '\n '
    # Send Message
    log = 'turno_trefila_report(admin)'
    log1 = 'turno_trefila_report(grupo_trefila)'
    Avbot.bot.send('anthony', msg, log)
    Avbot.bot.send('grupo_trefila', msg, log1)
    # Return True
    return True

##########################################################################################################################
#                                                       RHF ALARME                                                       #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_rhf_high_temp_alarm')
def pda_rhf_temp_alarm(req):
    if not Avbot.check(req, 'N', str): return False
    if not Avbot.check(req, 'GA', str): return False
    if not Avbot.check(req, 'valve', str): return False
    z = ''
    g = ''
    if req['N'] == '101': z = 'Pré Aquecimento'
    elif req['N'] == '102': z = 'Aquecimento'
    elif req['N'] == '103': z = 'Enxarque Superior'
    elif req['N'] == '104': z = 'Enxarque Inferior'
    else: return False
    if req['GA'] == 'G': g = 'Gás'
    elif req['GA'] == 'A': g = 'Ar'
    else: return False
    # Message
    msg = ' '.join(('*Atenção!* ⚠️ A temperatura está alta em uma Válvula',
        'de Regeneração da Linha de {} na Zona de {} do forno!')).format(g, z)
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_rhf_high_temp_alarm(admin)')
    # Grupo Manutencao
    Avbot.bot.send('laminador_mantenedores', msg, 'api::pda_rhf_high_temp_alarm(gm)')
    # Joao Paulo
    Avbot.bot.send('joao_paulo', msg, 'api::pda_rhf_high_temp_alarm(jp)')
    # Marcelo
    Avbot.bot.send('marcelo', msg, 'api::pda_rhf_high_temp_alarm(ms)')

##########################################################################################################################
#                                                   MILL AIR PRESS ALARM                                                 #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_mill_air_press_low')
def pda_mill_air_press_low(req):
    # Message
    msg = '*Atenção!* ⚠️ A pressão de Ar Comprimido do Laminador chegou abaixo de 4.5 Bar!'
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_mill_air_press_low(admin)')
    # Grupo Manutencao
    Avbot.bot.send('laminador_mantenedores', msg, 'api::pda_mill_air_press_low(gm)')
    # Joao Paulo
    Avbot.bot.send('joao_paulo', msg, 'api::pda_mill_air_press_low(jp)')
    # Marcelo
    Avbot.bot.send('marcelo', msg, 'api::pda_mill_air_press_low(ms)')

##########################################################################################################################
#                                                     TEMP NTM ALARME                                                    #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_rod_low_temp_alarm')
def pda_rod_low_temp_alarm(req):
    # Message
    msg = '*Atenção!* ⚠️ A temperatura chegou abaixo de 840 graus na entrada do bloco!'
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_rod_low_temp_alarm(admin)')
    # Grupo Automacao
    Avbot.bot.send('grupo_automation', msg, 'api::pda_rod_low_temp_alarm(gp)')
    # Marcelo
    Avbot.bot.send('marcelo', msg, 'api::pda_rod_low_temp_alarm(ms)')

##########################################################################################################################
#                                                     IPR SLIP ALARME                                                    #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_rod_ipr_slip_alarm')
def pda_rod_ipr_slip_alarm(req):
    if not Avbot.check(req, 'ipr', int): return False
    # Message
    msg = '*Atenção!* ⚠️ O pinch roll 0{} está patinando!'.format(req['ipr'])
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_rod_ipr_slip_alarm(admin)')
    # Grupo Automacao
    Avbot.bot.send('grupo_automation', msg, 'api::pda_rod_ipr_slip_alarm(gp)')
    # Marcelo
    Avbot.bot.send('marcelo', msg, 'api::pda_rod_ipr_slip_alarm(ms)')

##########################################################################################################################
#                                                   FISHLINE FLICK ALARME                                                #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_rod_fishline_flick_alarm')
def pda_rod_fishline_flick_alarm(req):
    if not Avbot.check(req, 'fl', int): return False
    fl = ('do Bloco' if req['fl'] == 1 else 'da Breakout Box')
    # Message
    msg = '*Atenção!* ⚠️ O Fishline {} piscou!'.format(fl)
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_rod_fishline_flick_alarm(admin)')
    # Grupo Automacao
    Avbot.bot.send('grupo_automation', msg, 'api::pda_rod_fishline_flick_alarm(gp)')
    # Joao Paulo
    Avbot.bot.send('joao_paulo', msg, 'api::pda_rod_fishline_flick_alarm(jp)')
    # Marcelo
    Avbot.bot.send('marcelo', msg, 'api::pda_rod_fishline_flick_alarm(ms)')

##########################################################################################################################
#                                                   LUB-C HIGH TEMP ALARME                                               #
##########################################################################################################################

# On Alarm
@Avbot.add('pda_rod_lubc_high_temp_alarm')
def pda_rod_lubc_high_temp_alarm(req):
    if not Avbot.check(req, 'temp', int): return False
    # Message
    msg = '*Atenção!* ⚠️ A temperatura do óleo da lub-C chegou acima de {} graus!'.format(req['temp'])
    # Admin
    Avbot.bot.send('anthony', msg, 'api::pda_rod_lubc_high_temp_alarm(admin)')
    # Grupo Automacao
    Avbot.bot.send('grupo_automation', msg, 'api::pda_rod_lubc_high_temp_alarm(gp)')
    # Joao Paulo
    Avbot.bot.send('joao_paulo', msg, 'api::pda_rod_lubc_high_temp_alarm(jp)')

##########################################################################################################################
#                                                      CLASSE TORQUE OFF                                                 #
##########################################################################################################################

# Class Torque Off
class TorqueOff:

    def __init__(self):
        # Data Variables
        self.s = [
            [],[],[],[],[],[],
            [],[],[],[],[],[],
            [],[],[],[],[],[]
        ]

    @property
    def bot(self): return Avbot.bot

    # Clear Torque
    def clear(self):
        t = self.bot.misc.datetime.datetime.now()
        for item in self.s:
            temp = self.bot.misc.copy.deepcopy(item)
            for e in item:
                t1 = t - self.bot.misc.datetime.timedelta(hours=1)
                if e <= t1: del temp[temp.index(e)]
            self.s[self.s.index(item)] = temp

    # Add Torque
    def add(self, std):
        self.clear()
        offset = std-1
        t = self.bot.misc.datetime.datetime.now()
        self.s[offset].append(t)
        return len(self.s[offset]) == 1

    # Torque Off
    @property
    def off(self):
        self.clear()
        cond = False
        off = list()
        for item in self.s:
            i = self.s.index(item)
            if len(item) > 0:
                off.append(dict(std=(i+1),
                stamps=item, times=len(item)))
            if len(item) > 1: cond = True
        return dict(off=off, cond=cond)

    # Torque Anormal Ultima Hora
    def send_off(self):
        m = self.off
        if type(m) != dict: return False
        if not m['cond']: return False
        m = m['off']
        msg = ' '.join(('Na ultima hora os torques das',
            'seguintes gaiolas ficaram fora do normal:'))
        for i in m:
            msg += '\nGaiola {}: {} vezes'.format(i['std'], i['times'])
        self.bot.send('anthony', msg, 'api::pda_mill_m_off(scheduled)')

# Instance Object
torqueOff = TorqueOff()

##########################################################################################################################
#                                                      TORQUE ALARME                                                     #
##########################################################################################################################

# Add API Get Torque Off
@Avbot.add('pda_mill_m_off', False)
def pda_mill_m_off(req):
    if not Avbot.check(req, 't', list): return False
    if not Avbot.check(req, 'std', (int, str)): return False
    # Insert data into MySQL
    cond = torqueOff.add(req['std'])
    if not cond: return True
    msg = '*Atenção!* ⚠️ O Torque da gaiola {} está anormal!'.format(req['std'])
    Avbot.bot.send('anthony', msg, 'api::pda_mill_m_off({})'.format(req['std']))
    return True

##########################################################################################################################
#                                                    ONE HOUR SCHEDULE                                                   #
##########################################################################################################################

@Avbot.bot.misc.schedule.each.one.hour.do.at('00:00')
def one_hour_scheudule():
    Avbot.bot.misc.requests.get('http://192.168.17.61:8085/misc/one_hour_schedule.php')
    # Avbot.bot.send('grupo_trefila', Lam.frio.prod(), 'schedule::lam.frio.prod(grupo_trefila)')
    # Avbot.bot.send('calegari', Lam.quente.prod(), 'schedule::lam.quente.prod(calegari)')
    torqueOff.send_off()

##########################################################################################################################
#                                                      KEEP ALIVE                                                        #
##########################################################################################################################

# Test Function
@Avbot.bot.misc.call.safe
def __test__():
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

# If Main
if __name__ == '__main__':
    # Start Avbot
    Avbot.start()
    # Test Bot
    __test__()
    # Keep Alive
    Avbot.keepalive()

##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################