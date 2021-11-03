
##########################################################################################################################

# Imports 
import re
import json
import copy
import datetime
from py_wapp import Bot
from py_misc import MySQL

# Modules
from . import stops

##########################################################################################################################
#                                                   PDA TREFILA STATUS                                                   #
##########################################################################################################################

# Load Actions
def __load__(bot: Bot, db: MySQL):
    
    ##########################################################################################################################

    # Status da Trefila
    @bot.add('pda_trf_status')
    def pda_trf_status(req):
        if not bot.check(req, 'mq', str): raise Exception('key "mq" not found')
        if not bot.check(req, 'status', str): raise Exception('key "status" not found')
        mq = req['mq']
        status = req['status']
        # Options Dictionary
        switcher = dict(
            stop = '😔 Máquina {} parada!‍',
            start = '😁 Máquina {} ligada!'
        )
        if status not in switcher: return False
        log = f'api::pda_trf_status({mq}, {status})'
        msg = switcher[status].format(mq)

        # Assemble Data
        starting = (status == 'start')
        dat = stops.assemble(mq, starting)
        
        ##########################################################################################################################

        # If Starting
        if starting:
            # Send Options Message
            if dat['stop'] != None:
                sec = dat['tempo_parado']
                d = datetime.timedelta(seconds=sec)
                parada = bot.chat.timedelta(d)
                msg += f'\n⏱️ {parada} de parada.'
            # Quest Group
            gmsg = copy.deepcopy(msg)
            msg_quest = stops.turno.chat.pergunta_parada
            gmsg += f'\n🗒️ {msg_quest} Escolha entre as opções da lista.'
            quote = stops.show_options(bot, 'anthony')
            # Send Message
            bot.send(to='jayron', text=msg, log=log)
            sent = bot.send(to='anthony', text=gmsg, log=log, quote=quote)
            # sent = bot.send(to='grupo_trefila', text=gmsg, log=log, quote=quote)
        else: # If Not Starting
            bot.send(to='jayron', text=msg, log=log)
            sent = bot.send(to='anthony', text=msg, log=log)
            # sent = bot.send(to='grupo_trefila', text=msg, log=log)

        # Insert to MySQL
        e = stops.insert_stop(db, dat, sent.id)
        
        ##########################################################################################################################

        # On Reply
        @sent.reply
        def add_cause(message):
            
            ##########################################################################################################################

            # On Ambiguous Message
            def ambiguous_msg(msg, has_float=False):
                r1 = (
                    'Sua mensagem não foi muito clara, evite o uso de',
                    'pontos ou vírgulas e não digite nenhum número que',
                    'não indique diretamente a causa da parada.'
                )
                r2 = (
                    'Se estiver tentando registrar a causa da parada de uma',
                    'máquina, digite um número que esteja na lista. Se houver',
                    'mais de uma causa, separe os números com Espaço.'
                )
                # check if has float
                ambig = ' '.join(r1 if has_float else r2)
                # Send Message
                log = 'sent_ambiguous_message'
                sent_ambig = bot.send(to='anthony', text=ambig, log=log, quote=msg.id)
                sent_ambig.reply(add_cause)
                return False
            
            ##########################################################################################################################

            # Verify Cause
            def verify_causas(msg):
                strin = bot.chat.clean(msg.body)
                char = re.findall('[a-zA-Z0-9]+', strin)
                num = re.findall('[0-9]+', strin)
                floats = re.findall('\d+\.\d+', strin)
                floats += re.findall('\d+\,\d+', strin)
                if len(char) == 0: return False
                if len(num) == 0: return ambiguous_msg(msg)
                if len(floats) > 0: return ambiguous_msg(msg, True)
                strin = re.sub('[^0-9]', ' ', strin)
                strin = bot.chat.clean(strin)
                causas = strin.split(' ')
                for i in range(len(causas)):
                    causas[i] = int(causas[i].lstrip('0'))
                return causas
            
            ##########################################################################################################################

            # Check for Existing Cause
            __cause__ = stops.get_cause(db, sent.id)
            
            ##########################################################################################################################

            # If Cause does not Exist
            if __cause__ == None:
                causas = verify_causas(message)
                if causas == False: return False
                causas_json = json.dumps(causas)
                stops.insert_cause(db, sent.id, causas_json)

            else: # If cause already Exists
                msg = stops.turno.chat.causa_ja_existe
                sent2 = message.quote(text=msg, log='trf_status_got_existing')
                # On Reply
                @sent2.reply
                def new_cause(confirm):
                    # On Affirmative
                    if bot.chat.yes(confirm):
                        causas = verify_causas(confirm)
                        if causas == False: return False
                        causas_json = json.dumps(causas)
                        stops.insert_cause(db, sent.id, causas_json)
                        sent2.reply(lambda: None)
                    # On Negative
                    elif bot.chat.no(confirm):
                        sent2.reply(lambda: None)
                    # On Neither
                    else: # Get Error Understanding
                        error = bot.chat.error.understand
                        sentL = confirm.quote(text=error, log='trf_status_didnt_got_it')
                        sentL.reply(new_cause)
                        
##########################################################################################################################
