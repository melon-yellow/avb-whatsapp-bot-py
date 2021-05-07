##########################################################################################################################
#                                                      AVBOT CORE                                                        #
##########################################################################################################################

# Bot Class
class Bot:

    # Init Bot
    def __init__(self):

        # Import Miscellaneous
        import sys
        sys.path.append('E:/python/misc')
        import miscellaneous

        # Instance Misc
        self.misc = miscellaneous.Miscellaneous()

        # Bot Phone Number
        self.id = ''

        # Allow Info
        bot = self.bot

        ##########################################################################################################################
        #                                                          ACTIONS                                                       #
        ##########################################################################################################################

        # Class Actions
        class Actions:

            # Init Actions
            def __init__(self, route, api):
                # Add API Execute Actions
                self.__api__ = api
                self.__route__ = self.__api__.add(route, methods=['GET', 'POST'])(self.__execute__)

                # Actions Dictionary
                self.__actions__ = dict()

            # Properties
            @property
            def bot(self): return bot

            @property
            def actions(self): return self

            # Set User
            def user(self, user):
                return self.__route__.user(user)

            # Set Pasword
            def password(self, password):
                return self.__route__.password(password)

            # Check Request
            def check(self, req, param, clas=None):
                cond = isinstance(req, dict) and isinstance(param, str) and param in req
                # Check Class
                if cond and self.bot.misc.inspect.isclass(clas):
                    try:  # Check for Iterable
                        iter(clas)
                        cond = any(isinstance(req[param], c) for c in clas)
                    except: cond = isinstance(req[param], clas)
                # Return Condtion
                return cond

            # Add Action
            def add(self, name, log=True):
                def __decorator__(function):
                    # Check Parameters
                    if (not callable(function)
                        or not isinstance(name, str)
                        or len(name) == 0):
                        return False
                    # Set Caller
                    function = self.bot.misc.call.safe(function)
                    function.__name__ = name
                    function.__logging__ = log
                    # Nest Objects
                    self.__actions__[name] = function
                    # Return Function
                    return function
                # Return Decorator
                return __decorator__

            # Append Actions
            def append(self, *args, **kwargs):
                # Append Iterator
                def __append__(col):
                    for act in col:
                        self.add(act)(col[act])

                # Args Append
                for arg in args:
                    # If is Dictionary
                    if isinstance(arg, dict):
                        __append__(arg)
                    # If is Iterable
                    elif isinstance(arg, list) or isinstance(arg, tuple):
                        for col in arg:
                            if isinstance(col, dict):
                                __append__(col)
                # Kwargs Append
                __append__(kwargs)
                # Return True
                return True

            # Execute Action
            def __execute__(self, req):
                data = None
                try: # Try Block
                    # Check Parameters
                    if not isinstance(req, dict): raise Exception('bad request')
                    if 'action' not in req: raise Exception('action missing in request')
                    if not isinstance(req['action'], str): raise Exception('action must be a string')
                    if len(req['action']) == 0: raise Exception('action not valid')
                    if req['action'] not in self.actions.__actions__: raise Exception('action not found')
                    # Get Action Name
                    action = req['action']
                    # Define Log
                    locale = self.__actions__[action].__locale__
                    ip = self.__api__.flask.request.remote_addr
                    log = 'Exec({}) From({})'.format(locale, ip)
                    # Log Action
                    if self.__actions__[action].__logging__:
                        self.bot.log(log)
                    # Execute Action
                    data = self.__actions__[action](req)
                # If Error Occurred
                except Exception as error:
                    return dict(done=False, error=str(error))
                try: # Make Serializable
                    json = self.bot.misc.json
                    serialize = lambda d: json.loads(json.dumps(d))
                    try: data = serialize(data)
                    except: data = serialize(data.__dict__)
                except: data = None
                # If Success
                return dict(done=True, data=data)

        ##########################################################################################################################
        #                                                         INTERFACE                                                      #
        ##########################################################################################################################

        # Interface Class
        class Interface:
            def __init__(self, actions):
                # Interface Actions Object
                self.actions = actions
                # Set Connection Status Object
                self.__conn__ = None

            @property
            def bot(self):
                return bot

            # Interface
            def req(self, req, ignore=False):
                # Check Parameters
                if not (self.__conn__ or ignore): return False
                try: # Try Request
                    r = self.bot.misc.requests.post(
                        'http://127.0.0.1:1615/bot',
                        auth=('bot', self.actions.__route__.__password__),
                        json=req,
                    )
                # Handle Error
                except: return False
                # Return Response
                return r

            @property
            def conn(self):
                try: # Try Block
                    r = self.req(None, True)
                    if r == False: raise Exception('Request Failed')
                    else: r.raise_for_status()
                except self.bot.misc.requests.exceptions.ConnectionError: return False
                except self.bot.misc.requests.exceptions.HTTPError: return False
                except self.bot.misc.requests.exceptions.Timeout: return False
                except: return False
                return True

            # Check Node Link
            def __link__(self):
                # Check for Changes
                conn = self.conn
                if self.__conn__ != conn:
                    self.__conn__ = conn
                    l1 = 'Connection with Node Established'
                    l2 = 'No Connection with Node'
                    log = l1 if conn else l2
                    self.bot.log(log)
                # Return Connection Status
                return self.__conn__

            # Add Action
            def add(self, name, log=True):
                return self.actions.add(name, log)

            # Start Interface App
            def start(self):
                # Check Link Cyclically
                self.bot.misc.schedule.each.one.second.do(self.__link__)
                try: # Get Bot Phone Number
                    req = self.req(dict(action='host_device'), True)
                    data = req.json()['data']
                    self.bot.id = data['wid']['user']
                except: return False
                return True
        
        ##########################################################################################################################
        #                                                           SQL                                                          #
        ##########################################################################################################################

        # SQL Class
        class SQL:

            # Init SQL
            def __init__(self):
                # Set MySQL Objects
                self.mysql = self.bot.misc.log.mysql
                self.user = self.mysql.kwargs['user']
                self.password = self.mysql.kwargs['password']
                # Set Connection Status Object
                self.__conn__ = None

            @property
            def bot(self):
                return bot

            # Check MySQL Link
            def __link__(self):
                conn = self.mysql.conn
                if self.__conn__ != conn:
                    self.__conn__ = conn
                    l1 = 'Connection with MySQL Established'
                    l2 = 'No Connection with MySQL'
                    log = l1 if conn else l2
                    self.bot.log(log)
                return self.__conn__

            # Start MySQL Connection
            def start(self):
                # Check Link Cyclically
                self.bot.misc.schedule.each.one.second.do(self.__link__)

        ##########################################################################################################################
        #                                                       MESSAGE CLASS                                                    #
        ##########################################################################################################################

        # Message Class
        class Message:
            def __init__(self):
                # Set Reply
                self.reply = self.Reply()
                # Constructor of Sent Messages
                self.sent = self.bot.misc.construct(self.Sent)

            @property
            def bot(self):
                return bot

            # Reply Class
            class Reply:
                def __init__(self):
                    # Set Replyables
                    self.__replyables__ = dict()
                    # Add Action
                    self.bot.interf.add('on_reply')(self.__execute__)

                @property
                def bot(self): return bot

                @property
                def msg(self):
                    return self.bot.message

                # Add Reply
                def add(self, msg_id, function):
                    # Check Parameters
                    if not callable(function):
                        return False
                    # Delete Old Replyable
                    try: del self.__replyables__[msg_id]
                    except: self.__replyables__[msg_id] = None
                    # Add to Dictionary
                    self.__replyables__[msg_id] = self.bot.misc.call.safe(function)
                    return True

                # On Reply
                def __execute__(self, req):
                    # Check Parameters
                    if (('msg_id' not in req)
                        or (req['msg_id'] not in self.__replyables__)
                        or ('reply' not in req)):
                        return False
                    # Get Reply
                    reply = req['reply']
                    msg_id = req['msg_id']
                    # Construct Reply
                    reply = self.msg.sent(reply)
                    # Execute Function
                    data = self.__replyables__[msg_id](reply)
                    # Return Data
                    return data

            # Sent Class
            class Sent:
                # Init Message
                def __init__(self, msg=None):

                    # Fix msg
                    if type(msg) != dict:
                        self.raw_data = {
                            'id': None,
                            'to': None,
                            'body': None,
                            'from': None,
                            'author': None,
                            'isGroupMsg': False,
                        }
                    else: self.raw_data = msg
                    # Set Default Reply
                    self.__reply__ = (lambda: None)
                    # Try Catch Block
                    try: # Get Quoted
                        q = self.raw_data['quotedMsgObj']
                        self.quoted = self.__class__(q)
                    except: q = None

                @property
                def bot(self): return bot
                @property
                def msg(self): return self.bot.message
                @property
                def id(self): return self.raw_data['id']
                @property
                def to(self): return self.raw_data['to']
                @property
                def body(self): return self.raw_data['body']
                @property
                def __from__(self): return self.raw_data['from']

                @property
                def author(self):
                    return (
                        self.raw_data['author']
                        if self.raw_data['isGroupMsg']
                        else self.raw_data['from']
                    )

                # On Reply
                def reply(self, function):
                    if type(self.id) != str: return function
                    self.__reply__ = self.bot.misc.call.safe(function)
                    self.msg.reply.add(self.id, self.__reply__)
                    return self.__reply__

                # Quote Message
                def quote(self, msg, log='api::quote_msg'):
                    return self.msg.send(self.__from__, msg, log, self.id)

            # Send Message
            def send(self, to, text, log='api::send_msg', quote_id=None):
                # Check Parameters
                if (not (isinstance(to, str) or to == None)
                    or not (isinstance(text, str) or text == None)
                    or not (isinstance(log, str) or log == None)
                    or not (isinstance(quote_id, str) or quote_id == None)):
                    return False
                # Interface Send Message
                sent = self.bot.interf.req(
                    dict(
                        action='send_msg',
                        to = to,
                        text = text,
                        log = log,
                        quote_id = quote_id,
                        reply_url = 'http://127.0.0.1:1516/ibot'
                    )
                )
                # On Interface Error
                if sent == False: return False
                # Convert to Json
                else: sent = sent.json()
                # Fix Errors
                if 'done' not in sent: return False
                if not sent['done']: return False
                # Construct Message
                sent = self.sent(sent['data'])
                # Logging
                log = 'api::send_msg' if type(log) != str else log
                self.bot.log('Sent({}) To({})'.format(log, to))
                # Return Sent
                return sent

            # Caller to Send
            def __call__(self, *args, **kwargs):
                return self.send(*args, **kwargs)

        ##########################################################################################################################
        #                                                      CHAT CLASS                                                        #
        ##########################################################################################################################

        # Chat Class
        class Chat:
            @property
            def bot(self): return bot

            # Clean Message
            def clean(self, message, lower=True):
                if isinstance(message, Message.Sent):
                    strin = self.bot.misc.copy.deepcopy(message.body)
                elif isinstance(message, str):
                    strin = self.bot.misc.copy.deepcopy(message)
                else: return False
                strin = strin.lower() if lower else strin
                strin = strin.replace(self.bot.id, '')
                while '  ' in strin:
                    strin = strin.replace('  ', ' ')
                strin = strin.strip()
                strin = self.bot.misc.unidecode.unidecode(strin)
                return strin

            # Check for Affirmative
            def yes(self, message=None):
                affirm = ['sim', 'positivo', 'correto', 'certo', 'isso']
                if message == None:
                    return self.bot.misc.random.choice(affirm)
                else:
                    return self.clean(message) in affirm

            # Check for Negative
            def no(self, message=None):
                neg = ['nao', 'negativo', 'errado']
                if message == None:
                    return self.bot.misc.random.choice(neg)
                else: return self.clean(message) in neg

            # Get Timedelta as String
            def timedelta(self, t):
                hd = t.seconds // 3600
                h = (t.days * 24) + hd
                m = (t.seconds - (hd * 3600)) // 60
                delta = '{} hora'.format(h) if h != 0 else ''
                delta += 's' if h > 1 else ''
                delta += ' e ' if h != 0 and m != 0 else ''
                delta += '{} minuto'.format(m) if m != 0 else ''
                delta += 's' if m > 1 else ''
                return delta

            @property
            def error(self):
                class Error:
                    @property
                    def bot(self):
                        return bot

                    @property
                    def understand(self):
                        p = [
                            'Desculpe, não entendi o que você quis dizer.',
                            'Sinceramente não entendi o que você falou.',
                            'Não fui capaz de interpretar o que você disse.',
                        ]
                        return self.bot.misc.random.choice(p)

                return Error()

        ##########################################################################################################################
        #                                                      NEST OBJECTS                                                      #
        ##########################################################################################################################

        # Set Bot Api
        self.api = self.misc.api(log=False).host('0.0.0.0').port(1516)

        # Set Bot Actions
        self.actions = Actions('/bot', self.api)
        self.actions.user('bot').password('vet89u43t0jw234erwedf21sd9R78fe2n2084u')

        # Set Bot Interface Actions
        iactions = Actions('/ibot', self.api)
        iactions.user('bot').password('ert2tyt3tQ3423rubu99ibasid8hya8da76sd')
        self.interf = Interface(iactions)

        # Set Global Objects
        self.message = Message()
        self.chat = Chat()
        self.sql = SQL()

        # Add Action Send
        @self.add('send_msg')
        def __send__(req):
            r = dict(to=None, text=None, log=None, id=None)
            if 'to' in req: r['to'] = req['to']
            if 'text' in req: r['text'] = req['text']
            if 'log' in req: r['log'] = req['log']
            if 'quote_id' in req: r['id'] = req['quote_id']
            sent = self.bot.send(r['to'], r['text'], r['log'], r['id'])
            return sent

    ##########################################################################################################################
    #                                                       BOT METHODS                                                      #
    ##########################################################################################################################

    @property
    def bot(self):
        return self

    # Add Action
    def add(self, name, log=True):
        return self.bot.actions.add(name, log)

    # Check Request
    def check(self, req, param, clas=None):
        return self.bot.actions.check(req, param, clas)

    # Logging
    def log(self, log):
        return self.bot.misc.log(log)

    # Start API App
    def start(self):
        # Start MySQL Connection
        self.bot.sql.start()
        self.bot.misc.time.sleep(0.1)
        # Start Bot Server
        s = self.bot.api.start()
        if not s: raise Exception('Server Not Started')
        self.bot.misc.time.sleep(0.1)
        # Start Interface Service
        i = self.bot.interf.start()
        if not i: raise Exception('Interface Not Started')
        self.bot.misc.time.sleep(0.1)
        # Log Finished
        self.bot.log('Avbot::Started')

    # Keep Alive
    def keepalive(self):
        self.bot.misc.keepalive()

    # Send Message
    def send(self, *args, **kwargs):
        return self.bot.message.send(*args, **kwargs)


##########################################################################################################################
#                                                         END                                                            #
##########################################################################################################################
