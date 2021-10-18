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
        # Generate List Message
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
        # Generate Message
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