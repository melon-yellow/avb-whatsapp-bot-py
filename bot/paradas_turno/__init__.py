
##########################################################################################################################

import py_misc
from py_wapp import Bot

##########################################################################################################################
#                                                     RELATORIO TURNO                                                    #
##########################################################################################################################

# Message Functions
class ChatTurno:
    
    # Init Turno
    def __init__(self, bot: Bot):
        self.bot = bot
        
    @property
    def misc(self):
        return self.bot.misc
    
    @property
    def pergunta_parada(self):
        p = ('Alguém pode me dizer o motivo da parada?',
            'Qual o motivo da parada?', 'Por que a máquina parou?',
            'Qual a justificativa da parada?')
        return self.misc.random.choice(p)
    
    @property
    def obtive_resposta(self):
        p = ('Ok', 'Entendi', 'Certo', 'Entendido', 'Registrado')
        return self.misc.random.choice(p)
    
    @property
    def obtive_nao(self):
        p = ('Ok', 'Entendi', 'Certo')
        return self.misc.random.choice(p)
    
    @property
    def causa_ja_existe(self):
        p = ('Uma informação referente à essa parada ja foi registrada',
            'Já encontrei registros desse horário', 'A causa dessa parada ja foi registrada')
        c = ('deseja substituir esse registro?', 'deseja registrar novamente?',
            'deseja refazer o registro?', 'deseja fazer um novo registro?')
        r = self.misc.random.choice(p) + ', ' + self.misc.random.choice(c)
        return r

##########################################################################################################################
#                                                     RELATORIO TURNO                                                    #
##########################################################################################################################

# Turno Class
class ClasseTurno:

    # Init Turno
    def __init__(
        self,
        bot: Bot,
        lam_db: py_misc.MySQL
    ):
        self.bot = bot
        self.lam_db = lam_db
        self.chat = ChatTurno(self.misc)
        
    @property
    def misc(self):
        return self.bot.misc

    @property
    def timestamp(self):
        return self.misc.datetime.datetime.now()

    @property
    def turma(self):
        sel = 0
        turmas = ['A','B','C','D']
        return turmas[sel]

    # Get Turno
    def turno(self, ts: py_misc.datetime.datetime = None):
        if ts == None: ts = self.timestamp
        y = (lambda t: ts.replace(hour=(t-1), minute=59, second=59, microsecond=999999))
        shift = dict(t0=y(8), t8=y(16), t16=y(24))
        for s in shift:
            if ts <= shift[s]:
                return int(s.replace('t',''))
            
##########################################################################################################################