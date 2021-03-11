
##########################################################################################################################
#                                                      MISCELLANEOUS                                                     #
##########################################################################################################################

# Miscellaneous Class
class Miscellaneous:

    # Init Miscellaneous
    def __init__(self):

        # Imports
        import json
        import copy
        import time
        import typing
        import pathlib
        import random
        import requests
        import flask
        import flask_httpauth
        import logging
        import queue
        import threading
        import schedule
        import dataclasses
        import mysql.connector
        import unicodedata
        import unidecode
        import datetime
        import builtins
        import inspect
        import signal
        import sys
        import os
        import re

        # Nest Miscellaneous Objects
        self.json = json
        self.copy = copy
        self.time = time
        self.typing = typing
        self.pathlib = pathlib
        self.random = random
        self.requests = requests
        self.flask = flask
        self.flask.httpauth = flask_httpauth
        self.logging = logging
        self.queue = queue
        self.threading = threading
        self.schedule = schedule
        self.dataclasses = dataclasses
        self.unicodedata = unicodedata
        self.unidecode = unidecode
        self.datetime = datetime
        self.builtins = builtins
        self.inspect = inspect
        self.signal = signal
        self.sys = sys
        self.os = os
        self.re = re

        #Allow Info
        misc = self.misc

##########################################################################################################################
#                                                        FIX IMPORTS                                                     #
##########################################################################################################################

        # Fix MySQL Connector
        class __mysql__:
            def __init__(self):
                self.__connector__ = mysql.connector
            @property
            def connector(self):
                return self.__connector__
        # Nest Objects
        self.__mysql__ = __mysql__()

##########################################################################################################################
#                                                         REFERENCE                                                      #
##########################################################################################################################

        # Reference to Miscellaneous
        class Misc:

            @property
            def misc(self): return misc

            @property
            def __locale__(self):
                return self.misc.locale(self)

##########################################################################################################################
#                                                        CONSTRUCTOR                                                     #
##########################################################################################################################

        # Class Constructor
        class Constructor(Misc):

            # Decorator
            def __init__(self, Class=type):
                self.__constructor__ = Class

            @property
            def __referer__(self):
                return self.__constructor__

            # Call Instancer
            def __call__(self, *args, **kwargs):
                return self.__constructor__(*args, **kwargs)

##########################################################################################################################
#                                                        DELTA TIME                                                      #
##########################################################################################################################

        # Delta Class
        class Delta(Misc):

            # Init Delta
            def __init__(self):
                self.since = self.Since()

            # Reset Delta
            def reset(self): self.since.reset()

            # Since Class
            class Since(Misc):

                # Init Since
                def __init__(self): self.reset()

                # Reset Delta
                def reset(self):
                    self.__start__ = self.misc.datetime.datetime.now()
                    self.__last__ = self.misc.datetime.datetime.now()
                    self.__delta__ = (self.__last__ - self.__start__)

                @property
                def init(self):
                    self.__last__ = self.misc.datetime.datetime.now()
                    return (self.__last__ - self.__start__)

                @property
                def last(self):
                    now = self.misc.datetime.datetime.now()
                    self.__delta__ = (now - self.__last__)
                    self.__last__ = now
                    return self.__delta__

##########################################################################################################################
#                                                            CALL                                                        #
##########################################################################################################################

        # Call Class
        class Call(Misc):

            # Check If Object Is a Caller
            def iscaller(self, obj=self):
                return (hasattr(obj, '__callable__') and
                    callable(obj.__callable__))

            # Check If Object Is a True Caller
            def istruecaller(self, obj=self):
                return (callable(obj) and self.iscaller(obj))

            # Get Callable of Object
            def getcallable(self, obj=self, bypass=False):
                caller = [obj]
                while (self.iscaller(caller[-1]) and ((caller[-1].__pass__
                    if hasattr(caller[-1], '__pass__') else False) or bypass)):
                    caller.append(caller[-1].__callable__)
                return caller[-1]

            # Check If Object Is a Resolvable
            def isresolvable(self, obj=self):
                return (self.iscaller(obj) and
                    all(hasattr(obj, attr) for attr in
                    ['__resolve__', 'value', 'resolved',
                    '__reject__', 'error', 'rejected',
                    '__reset__', 'resolution']))

            # Check If Object Is a Waitable
            def iswaitable(self, obj=self):
                return (self.isresolvable(obj) and
                    all(hasattr(obj, attr) for attr in
                    ['wait', 'then', 'catch',
                    '__thread__', '__trigger__']))

##########################################################################################################################
#                                                          CALLABLE                                                      #
##########################################################################################################################

        # Callable Class
        class Callable(Misc):

            # Init Callable
            def __init__(self, function):

                # Check Parameters
                if not callable(function):
                    self = False
                    return None

                # Nest Objects
                self.__callable__ = function

            @property
            def __referer__(self):
                return self.__callable__

            @property
            def __locale__(self):
                return self.misc.locale(self)


##########################################################################################################################
#                                                         RESOLVABLE                                                     #
##########################################################################################################################

        # Resolvable Class
        class Resolvable(Callable):

            # Init Resolvable
            def __init__(self, function, log=True):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(log, bool)):
                    self = False
                    return None

                # Init Callable
                super().__init__(function)

                # Set Status Attributes
                self.__resolved__ = False
                self.__rejected__ = False
                self.__value__ = None
                self.__error__ = None
                # Set Bypass
                self.__pass__ = True
                # Set Logging
                self.__log__ = None
                self.__logging__ = log

            @property
            def __bypass__(self):
                return (self.__pass__ and
                    issubclass(self.__callable__.__class__, Resolvable))

            @property
            def resolved(self):
                return (self.__callable__.resolved
                    if self.__bypass__ else self.__resolved__)

            @property
            def rejected(self):
                return (self.__callable__.rejected
                    if self.__bypass__ else self.__rejected__)

            @property
            def value(self):
                return (self.__callable__.value
                    if self.__bypass__ else self.__value__)

            @property
            def error(self):
                return (self.__callable__.error
                    if self.__bypass__ else self.__error__)

            @property
            def done(self):
                return (self.resolved or self.rejected)

            @property
            def resolution(self):
                return (self.value if self.resolved else
                    (self.error if self.rejected else None))

            # Resolve Method
            def __resolve__(self, value):
                if self.__bypass__:
                    try: self.__callable__.__resolve__(value)
                    except: pass
                self.__resolved__ = True
                self.__rejected__ = False
                self.__value__ = value
                self.__error__ = None
                # Return Value
                return self.value

            # Reject Method
            def __reject__(self, error):
                if self.__bypass__:
                    try: self.__callable__.__reject__(error)
                    except: pass
                self.__resolved__ = False
                self.__rejected__ = True
                self.__value__ = None
                self.__error__ = error
                self.__throw__()
                # Return Error
                return self.error

            # Reject Method
            def __reset__(self):
                if self.__bypass__:
                    self.__callable__.__reset__()
                # Reset Status
                self.__resolved__ = False
                self.__rejected__ = False
                self.__value__ = None
                self.__error__ = None
                return True

            # Throw Error
            def __throw__(self):
                # Set Error Log
                self.__log__ = ('Throw(' + self.__locale__ + ') ' +
                    'Catch(' + str(self.error) + ')')
                # Log Error
                self.__log__ = self.misc.log(self.__log__,
                    self.__logging__, self.__logging__)
                # Return Log
                return self.__log__

##########################################################################################################################
#                                                            SAFE                                                        #
##########################################################################################################################

        # Safe Class
        class Safe(Resolvable):

            # Init Safe
            def __init__(self, function, log=True):
                # Init Resolvable
                super().__init__(function, log)

            # Call Method
            def __call__(self, *args, **kwargs):
                # Reset Values
                self.__reset__()
                # Check If Callable Is Resolvable
                if self.__bypass__:
                    # Execute Callable
                    try: value = self.__callable__(*args, **kwargs)
                    except: pass
                    # Fix Resolution
                    if self.done: return self.resolution
                    # Exchange Resolution
                    self.__resolved__ = self.__callable__.resolved
                    self.__rejected__ = self.__callable__.rejected
                    self.__value__ = self.__callable__.value
                    self.__error__ = self.__callable__.error
                    # Return Resolution
                    return self.resolution
                else: # If Callable Is Not Resolvable
                    try: # Execute Callable
                        value = self.__callable__(*args, **kwargs)
                        # Fix Resolution
                        if self.done: return self.resolution
                        # Handle Resolve
                        try: self.__resolve__(value)
                        except: pass
                        return self.resolution
                    # On Error
                    except Exception as error:
                        # Fix Resolution
                        if self.done: return self.resolution
                        # Handle Reject
                        try: self.__reject__(error)
                        except: pass
                        return self.resolution
                # If Else
                return None

##########################################################################################################################
#                                                          CALLER                                                        #
##########################################################################################################################

        # Safe Class
        class Caller(Resolvable):

            # Init Safe
            def __init__(self, function, log=True):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(log, bool)):
                    self = False
                    return None

                # Init Resolvable
                function = self.misc.call.safe(function, log)
                super().__init__(function, log)

                # Set Default Caller
                self.call(lambda obj: obj.__callable__(*obj.args, **obj.kwargs))

                # Set Bypass to False
                self.__pass__ = False

                # Set Arguments
                self.args = list()
                self.iargs = list()
                self.kwargs = dict()
                self.ikwargs = dict()

            # Set Caller Arguments
            def setargs(self, *args, **kwargs):
                _params = (list(), dict())
                _call = self.misc.call.getcallable(self.__callable__)
                params = self.misc.inspect.getargspec(_call)[0]
                # Set Keyword Arguments
                for key in kwargs:
                    if key in params:
                        _params[1][key] = kwargs[key]
                        params.remove(key)
                # Set Var Arguments
                for arg in args:
                    if args.index(arg) < len(params):
                        _params[0].append(arg)
                # Set Arguments
                self.args = _params[0]
                self.kwargs = _params[1]
                return _params

            # Set Caller Function
            def call(self, function):
                if not callable(function): return False
                params = self.misc.inspect.getargspec(function)[0]
                if not len(params) == 1: return False
                function = self.misc.call.safe(function, self.__logging__)
                self.__caller__ = function
                return function

            # Call Method
            def __call__(self, *args, **kwargs):
                # Set Input Arguments
                self.iargs = args
                self.ikwargs = kwargs
                # Execute Caller
                return self.__caller__(self)

##########################################################################################################################
#                                                            TRY                                                         #
##########################################################################################################################

        # Try Class
        class Try(Resolvable):

            # Init Daemon
            def __init__(self, times=3, delay=1, timeout=60, function=None, condition=None):

                # Check Parameters
                if ((not isinstance(times, int) and times != None) or
                    (not isinstance(delay, int) and
                    not isinstance(delay, float) and delay != None) or
                    (not isinstance(timeout, int) and
                    not isinstance(timeout, float) and timeout != None) or
                    (function != None and not callable(function)) or
                    (condition != None and not callable(condition))):
                    self = False
                    return None

                # Fix None Functions
                if function == None: function = (lambda: None)
                if condition == None: condition = (lambda obj: obj.resolved)

                # Init Resolvable
                function = self.misc.call.safe(function, False)
                super().__init__(function, False)

                # Set Bypass to False
                self.__pass__ = False

                # Set Attempts Object
                self.__attempts__ = list()

                # Set Parameters
                self.__times__ = int(3)
                self.__delay__ = float(0)
                self.__delta__ = self.misc.time.delta()
                self.__timeout__ = self.misc.datetime.timedelta(seconds=60)

                # Call Setters
                self.times(times)
                self.delay(delay)
                self.timeout(timeout)
                self.condition(condition)

            # Times Setter
            def times(self, times):
                if (not isinstance(times, int) and
                    times != None): return False
                # Set Times
                self.__times__ = times
                # Return Self
                return self

            # Delay Setter
            def delay(self, delay):
                if (not isinstance(delay, int) and
                    not isinstance(delay, float) and
                    delay != None): return False
                # Fix None Delay
                if delay == None: delay = 0
                self.__delay__ = float(delay)
                # Return Self
                return self

            # Timeout Setter
            def timeout(self, timeout):
                td = self.misc.datetime.timedelta
                if (not isinstance(timeout, int) and
                    not isinstance(timeout, float) and
                    not isinstance(timeout, td) and
                    timeout != None): return False
                # Set Timeout
                if not isinstance(timeout, td) and timeout != None:
                    timeout = self.misc.datetime.timedelta(seconds=timeout)
                self.__timeout__ = timeout
                # Return Self
                return self

            # Set Callable
            def call(self, function):
                # Check Parameters
                if (not callable(function) and
                    function != None): return False
                # Fix None Function
                function = (function if function != None
                    else (lambda: None))
                function = self.misc.call.safe(function)
                self.__callable__ = function
                return function

            # Set Condition
            def condition(self, function):
                # Check Parameters
                if (not callable(function) and
                    function != None): return False
                # Fix None Function
                function = (function if function != None
                    else (lambda obj: obj.resolved))
                function = self.misc.call.safe(function)
                self.__condition__ = function
                return function

            # Caller to Try
            def __call__(self, *args, **kwargs):
                # Reset Delta
                self.__delta__.reset()
                # Try Loop
                while ((self.__times__ == None or
                    len(self.__attempts__) < self.__times__) and
                    (self.__timeout__ == None or
                    self.__delta__.since.init < self.__timeout__) and
                    not self.done):
                    # Execute Callable
                    value = self.__callable__(*args, **kwargs)
                    # Fix Delta
                    if self.__timeout__ == None: self.__delta__.reset()
                    # Fix List Length
                    if self.__times__ == None: self.__attempts__ = list()
                    # Append Attempt
                    self.__attempts__.append(dict(
                        resolved = self.__callable__.resolved,
                        rejected = self.__callable__.rejected,
                        value = self.__callable__.value,
                        error = self.__callable__.error))
                    # Compute Condition
                    condition = self.__condition__(self.__callable__)
                    if condition: self.__resolve__(value)
                    # Wait Delay
                    self.misc.time.sleep(self.__delay__)
                # Reject
                if not self.resolved:
                    self.__reject__('Max Attempts Exeeded')
                # Return Resolution
                return self.resolution

##########################################################################################################################
#                                                          DAEMON                                                        #
##########################################################################################################################

        # Daemon Class
        class Daemon(Resolvable):

            # Init Daemon
            def __init__(self, function, start=True, log=True):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(log, bool) or
                    not isinstance(start, bool)):
                    self = False
                    return None

                # Init Resolvable
                function = self.misc.call.safe(function, log)
                super().__init__(function, log)

                # Set Thread
                self.__thread__ = self.threading.Thread(target=self.__callable__)
                self.__thread__.daemon = True

                # Start Thread
                if start: self.start()

            @property
            def threading(self):
                return self.misc.threading

            @property
            def start(self):
                return self.__thread__.start

            @property
            def is_alive(self):
                return self.__thread__.is_alive

            @property
            def join(self):
                return self.__thread__.join

##########################################################################################################################
#                                                         PROMISE                                                        #
##########################################################################################################################

        # Promise Class
        class Promise(Daemon):

            # Init Promise
            def __init__(self, function, start=True):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(start, bool)):
                    self = False
                    return None

                # Set Caller
                self.__caller__ = self.misc.call.caller(function, log=False)
                self.__caller__.__pass__ = True

                # Set Caller Arguments
                self.__caller__.setargs(*self.args, **self.kwargs)

                # Set Caller Call
                @self.__caller__.call
                def __promise__(obj):
                    obj.__callable__(*obj.args, **obj.kwargs)
                    if self.resolved: self.__then__(self.value)
                    elif self.rejected: self.__catch__(self.error)

                # Preset Triggers
                self.then(lambda v: None)
                self.catch(lambda e: None)

                # Set Thread
                super().__init__(self.__caller__, start=start, log=False)

            # Resolve Method
            def __resolve__(self, value):
                super().__resolve__(value)
                raise Exception(value)

            # Reject Method
            def __reject__(self, error):
                super().__reject__(error)
                raise Exception(error)

            @property
            def args(self):
                return list((self.__resolve__,
                    self.__reject__))

            @property
            def kwargs(self):
                return dict(resolve = self.__resolve__,
                    reject = self.__reject__)

            # Then Trigger
            def then(self, function):
                return self.__settrig__(function, True)

            # Catch Trigger
            def catch(self, function):
                return self.__settrig__(function, False)

            # Set Trigger
            def __settrig__(self, function, resolve):
                # Nest Objects
                if not callable(function): return None
                function = self.misc.call.safe(function)
                if resolve: self.__then__ = function
                else: self.__catch__ = function
                # Return Thread
                return function

            # Promise Wait
            def wait(self):
                # Check If Thread Is Done
                while not self.done: pass
                # Return Resolution
                return self.resolution

##########################################################################################################################
#                                                           ASYNC                                                        #
##########################################################################################################################

        # Async Class
        class Async(Caller):

            # Init Async
            def __init__(self, function, log=False):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(log, bool)):
                    self = False
                    return None

                # Init Caller
                super().__init__(function, log)

                # Caller to Promise
                @self.call
                def __promise__(obj):
                    __caller__ = self.misc.call.caller(obj.__callable__)
                    __caller__.__pass__ = True
                    __caller__.setargs(*obj.iargs, **obj.ikwargs)
                    return self.threading.promise(__caller__)

            @property
            def threading(self):
                return self.misc.threading

##########################################################################################################################
#                                                            CYCLE                                                       #
##########################################################################################################################

        # Cycle Thread Class
        class Cycle(Daemon):

            # Init Now
            def __init__(self, function, delay=None, start=True):

                # Check Parameters
                if (not callable(function) or
                    not isinstance(start, bool)):
                    self = False
                    return None

                # Set Cyclic Try
                self.__try__ = self.misc.call.Try(function=function)
                self.__try__.times(None).delay(delay).timeout(None)
                self.__try__.condition(lambda obj: False)

                # Set Thread Object
                super().__init__(self.__try__, start=start, log=False)

##########################################################################################################################
#                                                           SERIAL                                                       #
##########################################################################################################################

        # Instant Scheduler Class
        class Serial(Cycle):

            # Init Now
            def __init__(self, start=True):

                # Check Parameters
                if not isinstance(start, bool):
                    self = False
                    return None

                # Define Execution Series
                self.__queue__ = self.queue.Queue()

                # Set Thread Object
                super().__init__(self.__pending__, start)

            @property
            def queue(self):
                return self.misc.queue

            # Run Pending
            def __pending__(self):
                if not self.__queue__.empty():
                    promise = self.__queue__.get()
                    promise.start()
                    promise.wait()

            # Add Functions
            def add(self, function):
                # Check for Callable
                if not callable(function): return False
                function = self.threading.promise(function, False)
                self.__queue__.put(function)
                # Return Promise
                return function

##########################################################################################################################
#                                                          SCHEDULE                                                      #
##########################################################################################################################

        # Each Class
        class Each(Misc):

            # Properties
            @property
            def one(self): return self.Every(1)
            @property
            def two(self): return self.Every(2)
            @property
            def three(self): return self.Every(3)
            @property
            def four(self): return self.Every(4)
            @property
            def five(self): return self.Every(5)
            @property
            def six(self): return self.Every(6)
            @property
            def seven(self): return self.Every(7)
            @property
            def eight(self): return self.Every(8)
            @property
            def nine(self): return self.Every(9)
            @property
            def ten(self): return self.Every(10)

            # Every Class
            class Every(Misc):

                # Init Every
                def __init__(self, step):
                    self.step = step

                @property
                def schedule(self): return self.misc.schedule
                @property
                def every(self): return self.schedule.every(self.step)
                @property
                def second(self): return self.Period('second', self.every)
                @property
                def seconds(self): return self.Period('seconds', self.every)
                @property
                def minute(self): return self.Period('minute', self.every)
                @property
                def minutes(self): return self.Period('minutes', self.every)
                @property
                def hour(self): return self.Period('hour', self.every)
                @property
                def hours(self): return self.Period('hours', self.every)
                @property
                def day(self): return self.Period('day', self.every)
                @property
                def days(self): return self.Period('days', self.every)
                @property
                def week(self): return self.Period('week', self.every)
                @property
                def weeks(self): return self.Period('weeks', self.every)

                # Period Class
                class Period(Misc):

                    # Init Period
                    def __init__(self, period, every):
                        self.period = period
                        self.every = every

                    @property
                    def do(self):
                        return self.Do(self.period, self.every)

                    # Do Class
                    class Do(Misc):

                        # Init Do
                        def __init__(self, period, every):
                            self.period = period
                            self.every = every

                        @property
                        def __act__(self):
                            return getattr(self.every, self.period)

                        # Do At
                        def at(self, time):
                            def __decorator__(function):
                                if not callable(function): return False
                                function = self.misc.call.safe(function)
                                fasync = self.misc.threading.Async(function)
                                self.__act__.at(time).do(fasync)
                                return function
                            return __decorator__

                        # Do
                        def __call__(self, function):
                            if not callable(function): return False
                            function = self.misc.call.safe(function)
                            fasync = self.misc.threading.Async(function)
                            self.__act__.do(fasync)
                            return function

##########################################################################################################################
#                                                           MySQL                                                        #
##########################################################################################################################

        # Class MySQL
        class MySQL(Misc):

            # Init MySQL
            def __init__(self, *args, **kwargs):

                # Set References
                self.args = args
                self.kwargs = kwargs

                # Start Thread
                self.__series__ = self.misc.threading.serial()

            @property
            def connector(self):
                return self.misc.__mysql__.connector

            @property
            def conn(self):
                try: # Check for mydb
                    mydb = self.__connect__()
                    conn = mydb.is_connected()
                    mydb.close()
                    return conn
                except: return False

            @property
            def mydb(self):
                if not self.conn: return False
                try: return self.__connect__()
                except: return False

            # Connect
            def __connect__(self):
                return self.connector.connect(*self.args, **self.kwargs)

            # Get Data From DB
            def get(self, query):
                @self.__series__.add
                def __fetch__(resolve, reject):
                    mydb = self.mydb
                    if mydb == False: reject(False)
                    cursor = mydb.cursor()
                    cursor.execute(query)
                    data = cursor.fetchall()
                    cursor.close()
                    mydb.close()
                    data = list(map(lambda i: list(i), list(data)))
                    if not isinstance(data, list): data = list()
                    resolve(data)
                # Return Resolution
                return __fetch__.wait()

            #  Execute Into DB
            def execute(self, query, val=tuple()):
                @self.__series__.add
                def __execute__(resolve, reject):
                    mydb = self.mydb
                    if mydb == False: reject(False)
                    cursor = mydb.cursor()
                    cursor.execute(query, val)
                    mydb.commit()
                    cursor.close()
                    mydb.close()
                    resolve(True)
                # Return Resolution
                return __execute__.wait()

##########################################################################################################################
#                                                           LOGS                                                         #
##########################################################################################################################

        # Logs Class
        class Logs(Misc):

            # Init Logs
            def __init__(self):

                # Set Consturctor
                self.__constructor__ = self.misc.construct(self.Log)

                # Define Authentication
                self.user = 'root'
                self.password = 'vet89u43t0jw234erwedf21sd9R78fe2n2084u'

                # Append Object
                self.mysql = self.misc.mysql(
                    host = '127.0.0.1', port = '1517', user = self.user,
                    password = self.password, database = 'bot')

            # Log Class
            class Log(Misc):

                # Init Log
                def __init__(self, log, console=True, mysql=True):

                    # Check Parameters
                    if (not isinstance(log, str) or
                        not isinstance(mysql, bool) or
                        not isinstance(console, bool)):
                        self = False
                        return None

                    # Get Timestamp
                    self.__timestamp__ = self.misc.datetime.datetime.now()
                    self.__log__ = self.misc.copy.deepcopy(log)

                    # Execute
                    if not self.logs.mysql.conn: mysql = False
                    if mysql: self.__mysql__()
                    if console: self()

                @property
                def logs(self): return self.misc.log

                @property
                def __t__(self):
                    t = self.__timestamp__
                    t =  t.strftime('%m/%d/%Y, %H:%M:%S')
                    t = '({})'.format(t)
                    return t

                @property
                def __error__(self):
                    if self.logs.mysql.conn: return ''
                    else: return '(MySQL Error)'

                # Log to MySQL
                def __mysql__(self):
                    query = 'INSERT INTO logs (Timestamp, App, Log) VALUES (%s, %s, %s)'
                    schema = self.misc.__schema__
                    val = (self.__timestamp__, schema, self.__log__)
                    e = self.logs.mysql.execute(query, val)
                    return e

                # String Representation
                def __str__(self):
                    strin = ' '.join((self.__t__,
                        self.__log__, self.__error__))
                    strin = strin.strip()
                    return strin

                # Caller to Console Log
                def __call__(self):
                    print(str(self))

            # Instance Object
            def __call__(self, *args, **kwargs):
                return self.__constructor__(*args, **kwargs)

##########################################################################################################################
#                                                            API                                                         #
##########################################################################################################################

        # API Class
        class API(Misc):

            # Init API
            def __init__(self, log=False):

                # Check Parameters
                if not isinstance(log, bool):
                    self = False
                    return None

                # Define App
                self.__app__ = self.flask.Flask(__name__)

                # Remove Flask Logging
                if not log:
                    self.__app__.logger.disabled = True
                    self.misc.logging.getLogger('werkzeug').disabled = True

                # Set Routes Dictionary
                self.__routes__ = dict()

                # Set Server Params
                self.host(None).port(None)

            @property
            def flask(self):
                return self.misc.flask

            @property
            def httpauth(self):
                return self.misc.flask.httpauth

            # Set Host
            def host(self, host):
                self.__host__ = host
                return self

            # Set Port
            def port(self, port):
                self.__port__ = port
                return self

            # Route Class
            class Route(Callable):
                # Init Route
                def __init__(self, function, route, api, methods):
                    # Check for Callable
                    if (not callable(function) or
                        not isinstance(route, str)):
                        self = False
                        return None
                    # Set Callable
                    self.__callable__ = self.misc.call.safe(function)
                    # Set API
                    self.__api__ = api
                    self.__route__ = str(route)
                    self.__auth__ = self.__api__.httpauth.HTTPBasicAuth()
                    # Set Auth Params
                    self.user(None).password(None)
                    # Auth Verify
                    @self.__auth__.verify_password
                    def __auth__(user, password):
                        a = (self.__user__ == user or
                            self.__user__ == None)
                        b = (self.__password__ == password or
                            self.__password__ == None)
                        if a and b: return user
                    # Create Dynamic Named Function
                    def __route__():
                        json = self.__api__.flask.request.json
                        data = self.__callable__(json)
                        return self.__api__.flask.jsonify(data)
                    __route__.__name__ = route.replace('/','')
                    # Route Flask App
                    self.__api__.__app__.route(self.__route__, methods=methods)(
                        self.__auth__.login_required(__route__)
                    )

                # Set User
                def user(self, user):
                    self.__user__ = user
                    return self

                # Set Password
                def password(self, password):
                    self.__password__ = password
                    return self

            # Add Route to App
            def add(self, route, methods=['GET', 'POST']):
                def __decorator__(function):
                    if (not callable(function) or
                        not isinstance(route, str)): return False
                    __route__ = self.Route(function, route, self, methods)
                    self.__routes__[route] = __route__
                    return __route__
                # Return Decorator
                return __decorator__

            # Start App
            def start(self):
                # Check for Host and Port
                if (self.__host__ == None or
                    self.__port__ == None): return False
                try: # Start Server on Daemon Thread
                    self.__thread__ = self.misc.threading.daemon(
                        lambda: self.__app__.run(host=self.__host__, port=self.__port__)
                    )
                except: return False
                # Return True
                return True

##########################################################################################################################
#                                                       NEST OBJECTS                                                     #
##########################################################################################################################

        # Misc
        self.Misc = Misc

        # Constructor
        self.construct = Constructor

        # Time Delta
        self.time.delta = self.construct(Delta)

        # Call
        self.call = Call()
        self.call.Callable = self.construct(Callable)
        self.call.safe = self.construct(Safe)
        self.call.caller = self.construct(Caller)
        self.call.Try = self.construct(Try)

        # Threading
        self.threading.daemon = self.construct(Daemon)
        self.threading.promise = self.construct(Promise)
        self.threading.Async = self.construct(Async)
        self.threading.cycle = self.construct(Cycle)
        self.threading.serial = self.construct(Serial)
        self.threading.is_main = (lambda:
            self.threading.current_thread() is
            self.threading.main_thread())

        # MySQL
        self.mysql = self.construct(MySQL)

        # Logging
        self.log = Logs()

        # API
        self.api = self.construct(API)

        # Schedule
        self.schedule.each = Each()
        self.schedule.__thread__ = self.threading.cycle(
            self.schedule.run_pending, delay=1)

##########################################################################################################################
#                                                       MISC METHODS                                                     #
##########################################################################################################################

    @property
    def misc(self): return self

    # Get Location of Main Script
    @property
    def __schema__(self):
        path = self.sys.modules['__main__'].__file__
        path = self.os.path.abspath(path)
        return path

    # Get Referer Object
    def referer(self, obj):
        referer = [obj]
        while hasattr(referer[-1], '__referer__'):
            referer.append(referer[-1].__referer__)
        return referer[-1]

    # Get Location of Object in Script
    def locale(self, obj):
        referer = self.referer(obj)
        module = referer.__module__ if hasattr(referer, '__module__') else '__main__'
        module = module if module.startswith('__main__') else '::'.join(('__main__', module))
        qual = referer.__qualname__ if hasattr(referer, '__qualname__') else '__?__'
        locale = '::'.join((module, qual))
        locale = locale.replace('.<locals>.', '::')
        return locale

    # Keep Alive
    def keepalive(self):
        try: # Keep Main Thread Alive
            while True: pass
        except KeyboardInterrupt: pass

##########################################################################################################################
#                                                           END                                                          #
##########################################################################################################################
