##########################################################################################################################
#                                                   PDA TREFILA STATUS                                                   #
##########################################################################################################################

# Status da Trefila
@Avbot.add('pda_trf_status')
def pda_trf_status(req):
    if not Avbot.check(req, 'mq', str): raise Exception('key "mq" not found')
    if not Avbot.check(req, 'status', str): raise Exception('key "status" not found')
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
        msg_quest = stopTref.turno.chat.pergunta_parada
        gmsg += '\n🗒️ {} Escolha entre as opções da lista.'.format(msg_quest)
        quote = stopTref.show_options('anthony')
        # Send Message
        Avbot.bot.send('jayron', msg, log)
        # Avbot.bot.send('anthony', msg, log)
        # sent = Avbot.bot.send('grupo_trefila', gmsg, log, quote)
        sent = Avbot.bot.send('anthony', gmsg, log, quote)
    else: # If Not Starting
        Avbot.bot.send('jayron', msg, log)
        sent = Avbot.bot.send('anthony', msg, log)

    # Insert to MySQL
    e = stopTref.insert_stop(dat, sent.id)

    # On Reply
    @sent.reply
    def add_cause(message):

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
                    causas = verify_causas(confirm)
                    if causas == False: return False
                    causas_json = Avbot.bot.misc.json.dumps(causas)
                    stopTref.insert_cause(sent.id, causas_json)
                    sent2.reply(lambda: None)
                # On Negative
                elif Avbot.bot.chat.no(confirm):
                    sent2.reply(lambda: None)
                # On Neither
                else: # Get Error Understanding
                    error = Avbot.bot.chat.error.understand
                    sentL = confirm.quote(error, 'trf_status_didnt_got_it')
                    sentL.reply(new_cause)