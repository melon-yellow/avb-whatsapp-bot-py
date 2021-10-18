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
            p = ('Alguém pode me dizer o motivo da parada?',
                'Qual o motivo da parada?', 'Por que a máquina parou?',
                'Qual a justificativa da parada?')
            return self.bot.misc.random.choice(p)

        @property
        def obtive_resposta(self):
            p = ('Ok', 'Entendi', 'Certo', 'Entendido', 'Registrado')
            return self.bot.misc.random.choice(p)

        @property
        def obtive_nao(self):
            p = ('Ok', 'Entendi', 'Certo')
            return self.bot.misc.random.choice(p)

        @property
        def causa_ja_existe(self):
            p = ('Uma informação referente à essa parada ja foi registrada',
                'Já encontrei registros desse horário', 'A causa dessa parada ja foi registrada')
            c = ('deseja substituir esse registro?', 'deseja registrar novamente?',
                'deseja refazer o registro?', 'deseja fazer um novo registro?')
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