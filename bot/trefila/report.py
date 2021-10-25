
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
def __load__(bot: Bot, lam_db: MySQL):
    
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
        def qur(tb):
            return ' '.join(('SELECT * FROM `{}` WHERE (`turno` = {}',
                'AND `date` = \'{}\') ORDER BY `timestamp`')).format(tb, t, d)
        # Get queries
        query1 = qur('lam_frio_interr_turno')
        query2 = qur('lam_frio_interr_causa')

        # Execute Query
        paradas = lam_db.get(query1)
        causas = lam_db.get(query2)
        
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
                'WHERE (message_id = \'{}\' OR message_id = \'{}\')',
                'ORDER BY `timestamp` DESC')).format(item[7], item[8])
            # Execute Query
            cause = lam_db.get(query)
            cause = list() if len(cause) == 0 else cause[0]
            if len(cause) > 0: cause = json.loads(cause[4])
            return cause

        # Create Message
        def turn(h):
            return '{}{}:00'.format('0' if len(str(h)) < 2 else '', h)

        # get stop duration
        def format_dur(item):
            if item[6] != None:
                delt = datetime.timedelta(seconds=item[6])
                return bot.chat.timedelta(delt)
            else: return 'duração indeterminada'

        # get stop cause
        def format_cause(item):
            ca = get_cause(item)
            if len(ca) == 0: return 'causa não declarada'
            cause = ''
            op = stops.get_options(lam_db)
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
            '📋 *Produção dia {}*'.format(d.strftime('%d/%m/%Y')),
            '🕒 *Turno das {} às {}*'.format(turn(t), turn(t+8)),
            '🔠 *Turma {}*'.format(turma),
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
                paradas.append('⚠️ Parada de {} por {}'.format(
                    format_dur(item), format_cause(item)
                ))
            # append div to message
            msg += '\n'.join((
                '',
                '*Máquina {}:*'.format(1 + paradas.index(maquina)),
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
            lam_db.execute(query, val)

        # Iterate over Util
        for i in range(5):
            insert_util_turno(i+1)

        # Get Shift Util
        def get_util_turno(util):
            # get data from last shift
            query_last_turno = ' '.join(('SELECT * FROM `lam_frio_util`',
                'WHERE (`turno` = {} AND `date` = \'{}\')',
                'ORDER BY `mq`')).format(t-8, d)
            last_turno = lam_db.get(query_last_turno)
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
            '📊 Utilização M2 (Turno): {}%'.format(ut['u2']),
            '📊 Utilização M3 (Turno): {}%'.format(ut['u3']),
            '📊 Utilização M4 (Turno): {}%'.format(ut['u4']),
            '📊 Utilização M5 (Turno): {}%'.format(ut['u5']),
            '📊 *Utilização Global: {}%*'.format(ut['u']),
            '------------------------------------------------------',
            '*Tempo Parado:*',
            '------------------------------------------------------',
            '⚠️ Tempo parado M2 (Turno): {}'.format(ut['t2']),
            '⚠️ Tempo parado M3 (Turno): {}'.format(ut['t3']),
            '⚠️ Tempo parado M4 (Turno): {}'.format(ut['t4']),
            '⚠️ Tempo parado M5 (Turno): {}'.format(ut['t5']),
            '⚠️ *Paradas Totais no Turno: {}*'.format(ut['t']),
            '------------------------------------------------------',
            ''
        ))
        
        ##########################################################################################################################

        # log
        log = 'turno_trefila_report'
        # send message
        if send_report:
            # bot.send('grupo_trefila', msg, log)
            bot.send('anthony', msg, log)
            bot.send('jayron', msg, log)
        # Return True
        return True
    
##########################################################################################################################
