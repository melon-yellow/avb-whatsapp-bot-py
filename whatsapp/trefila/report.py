
##########################################################################################################################

# Imports
import json
import copy
import datetime
from py_wapp import Bot
from py_misc import MySQL

# Modules
from . import stops
from .. import iba

##########################################################################################################################
#                                                    REPORT TREFILA TURNO                                                #
##########################################################################################################################

# Load Actions
def __load__(bot: Bot, db: MySQL):
    
    ##########################################################################################################################

    # Relatorio Turno Trefila
    @bot.add('pda_trf_report')
    def pda_trf_report(req):
        if not bot.check(req, 't', list): raise Exception('key "t" not found')
        if not bot.check(req, 'util', list): raise Exception('key "util" not found')
        t_pda = iba.methods.timestamp(req['t'])
        util = req['util']

        # Get Shift and Date
        d = t_pda.date()
        t = t_pda.hour
        turma = stops.turno.get_turma()

        # Fix Shift
        if 7 <= t and t <= 9: t = 0
        elif 15 <= t and t <= 17: t = 8
        elif 23 <= t or t <= 1: t = 16
        else: return False

        # Fix Date
        if t == 16:
            d -= datetime.timedelta(days=1)

        # Create Query
        makequery = (lambda tb: ' '.join((
            f'SELECT * FROM `{tb}` WHERE (`turno` = {t}',
            f'AND `date` = \'{d}\') ORDER BY `timestamp`'
            ))
        )
        # Get queries
        query1 = makequery('lam_frio_interr_turno')
        query2 = makequery('lam_frio_interr_causa')

        # Execute Query
        paradas = db.get(query1)
        causas = db.get(query2)
        
        ##########################################################################################################################

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
        paradas = copy.deepcopy(temp)
        temp = [list(),list(),list(),list(),list()]

        # Filter by Machine
        for item in paradas: temp[item[3]-1].append(item)
        paradas = copy.deepcopy(temp)
        
        ##########################################################################################################################

        def get_cause(item):
            if item[7] == None: item[7] = 'NULL'
            if item[8] == None: item[8] = 'NULL'
            # Create Query
            query = ' '.join(('SELECT * FROM `lam_frio_interr_causa`',
                f'WHERE (message_id = \'{item[7]}\' OR message_id = \'{item[8]}\')',
                'ORDER BY `timestamp` DESC'))
            # Execute Query
            cause = db.get(query)
            cause = list() if len(cause) == 0 else cause[0]
            if len(cause) > 0: cause = json.loads(cause[4])
            return cause

        # Create Message
        def turn(h):
            return '0' if len(str(h)) < 2 else '' + f'{h}:00'

        # get stop duration
        def _dur(item):
            if item[6] != None:
                delt = datetime.timedelta(seconds=item[6])
                return bot.chat.timedelta(delt)
            else: return 'duração indeterminada'

        # get stop cause
        def _cause(item):
            ca = get_cause(item)
            if len(ca) == 0: return 'causa não declarada'
            cause = ''
            op = stops.get_options(db)
            op[0][1] = 'causa não listada'
            for c in range(len(ca)):
                sep = ('' if c == 0 else (' e ' if (c == len(ca) - 1) else ', '))
                for o in range(len(op)):
                    if ca[c] != op[o][0]: continue
                    thisc = sep + op[o][1]
                cause += thisc.lower()
            return cause

        # conditon to send report
        send_report = True
        
        ##########################################################################################################################

        # Title
        msg = '\n'.join(('',
            '------------------------------------------------------',
            '🤖 *Relatório de Paradas Trefila* 👾',
            '------------------------------------------------------',
            f'📋 *Produção dia {d.strftime("%d/%m/%Y")}*',
            f'🕒 *Turno das {turn(t)} às {turn(t + 8)}*',
            f'🔠 *Turma {turma}*',
            '------------------------------------------------------'
        ))

        # Iterate Over Machines
        for maquina in paradas:
            # check for stops
            if len(maquina) == 0: continue
            # Iterate Over Stops
            paradas = []
            for item in maquina:
                # append stop
                paradas.append(f'⚠️ Parada de {_dur(item)} por {_cause(item)}')
            # append div to message
            msg += '\n'.join((
                '',
                f'*Máquina {1 + paradas.index(maquina)}:*',
                '------------------------------------------------------',
                '\n'.join(paradas),
                '------------------------------------------------------'
            ))
            
        ##########################################################################################################################

        # Insert Turno Util
        def insert_util_turno(mq):
            query = ' '.join(('INSERT INTO `lam_frio_util`',
                '(`timestamp`, `date`, `turno`, `mq`, `sec`, `util`)',
                'VALUES (%s, %s, %s, %s, %s, %s)'))
            val = (t_pda, d, t, mq, util[0], util[mq])
            db.execute(query, val)

        # Iterate over Util
        for i in range(5):
            insert_util_turno(i+1)

        # Get Shift Util
        def get_util_turno(util):
            # get data from last shift
            query_last_turno = ' '.join(('SELECT * FROM `lam_frio_util`',
                f'WHERE (`turno` = {t - 8} AND `date` = \'{d}\')',
                'ORDER BY `mq`'))
            last_turno = db.get(query_last_turno)
            # Check for Data
            if len(last_turno) == 0:
                send_report = False
                return
            # Fix util ref
            util[0] = 28800
            # Iterate over Data
            for i in range(5):
                # Iterate over Util
                for row in last_turno:
                    if row[3] == i+1:
                        util[i+1] -= row[5]
                        break
            # return util fixed
            return util

        if t > 0: # If shift > 0
            util = get_util_turno(util)
            
        ##########################################################################################################################

        # Format Util
        ut = dict()
        # Calc Util
        ut['u1'] = ((util[1] / util[0]) * 100)
        ut['u2'] = ((util[2] / util[0]) * 100)
        ut['u3'] = ((util[3] / util[0]) * 100)
        ut['u4'] = ((util[4] / util[0]) * 100)
        ut['u5'] = ((util[5] / util[0]) * 100)
        ut['u'] = ((ut['u2'] + ut['u3'] + ut['u4'] + ut['u5']) / 4)
        # Verify Util
        if not (0 <= ut['u1'] <= 100): send_report = False
        if not (0 <= ut['u2'] <= 100): send_report = False
        if not (0 <= ut['u3'] <= 100): send_report = False
        if not (0 <= ut['u4'] <= 100): send_report = False
        if not (0 <= ut['u5'] <= 100): send_report = False
        if not (0 <= ut['u'] <= 100): send_report = False
        # Fix Util
        ut['u1'] = str(round(ut['u1'], 2))
        ut['u2'] = str(round(ut['u2'], 2))
        ut['u3'] = str(round(ut['u3'], 2))
        ut['u4'] = str(round(ut['u4'], 2))
        ut['u5'] = str(round(ut['u5'], 2))
        ut['u'] = str(round(ut['u'], 2))
        # Calc Time
        ut['t1'] = datetime.timedelta(seconds=(util[0] - util[1]))
        ut['t2'] = datetime.timedelta(seconds=(util[0] - util[2]))
        ut['t3'] = datetime.timedelta(seconds=(util[0] - util[3]))
        ut['t4'] = datetime.timedelta(seconds=(util[0] - util[4]))
        ut['t5'] = datetime.timedelta(seconds=(util[0] - util[5]))
        ut['t'] = (ut['t2'] + ut['t3'] + ut['t4'] + ut['t5'])
        # Verify Time
        zt = datetime.timedelta(seconds=0)
        ht = datetime.timedelta(seconds=28800)
        ft = datetime.timedelta(seconds=4*28800)
        if not (zt <= ut['t1'] <= ht): send_report = False
        if not (zt <= ut['t2'] <= ht): send_report = False
        if not (zt <= ut['t3'] <= ht): send_report = False
        if not (zt <= ut['t4'] <= ht): send_report = False
        if not (zt <= ut['t5'] <= ht): send_report = False
        if not (zt <= ut['t'] <= ft): send_report = False
        # Fix Time
        ut['t1'] = bot.chat.timedelta(ut['t1'])
        ut['t2'] = bot.chat.timedelta(ut['t2'])
        ut['t3'] = bot.chat.timedelta(ut['t3'])
        ut['t4'] = bot.chat.timedelta(ut['t4'])
        ut['t5'] = bot.chat.timedelta(ut['t5'])
        ut['t'] = bot.chat.timedelta(ut['t'])
        
        ##########################################################################################################################

        # Append Util
        msg += '\n'.join((
            '',
            '*Utilização:*',
            '------------------------------------------------------',
            f'📊 Utilização M2 (Turno): {ut["u2"]}%',
            f'📊 Utilização M3 (Turno): {ut["u3"]}%',
            f'📊 Utilização M4 (Turno): {ut["u4"]}%',
            f'📊 Utilização M5 (Turno): {ut["u5"]}%',
            f'📊 *Utilização Global: {ut["u"]}%*',
            '------------------------------------------------------',
            '*Tempo Parado:*',
            '------------------------------------------------------',
            f'⚠️ Tempo parado M2 (Turno): {ut["t2"]}',
            f'⚠️ Tempo parado M3 (Turno): {ut["t3"]}',
            f'⚠️ Tempo parado M4 (Turno): {ut["t4"]}',
            f'⚠️ Tempo parado M5 (Turno): {ut["t5"]}',
            f'⚠️ *Paradas Totais no Turno: {ut["t"]}*',
            '------------------------------------------------------',
            ''
        ))
        
        ##########################################################################################################################

        # log
        log = 'turno_trefila_report'
        # send message
        if send_report:
            # bot.send(to='grupo_trefila', text=msg, log=log)
            bot.send(to='anthony', text=msg, log=log)
            bot.send(to='jayron', text=msg, log=log)
        # Return True
        return True
    
##########################################################################################################################
