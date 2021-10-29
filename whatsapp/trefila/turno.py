
##########################################################################################################################

import random
import datetime
from typing import Literal

##########################################################################################################################
#                                                     RELATORIO TURNO                                                    #
##########################################################################################################################

# Message Functions
class ChatTurno:
    
    @property
    def pergunta_parada(self):
        p = ('Alguém pode me dizer o motivo da parada?',
            'Qual o motivo da parada?', 'Por que a máquina parou?',
            'Qual a justificativa da parada?')
        return random.choice(p)
    
    @property
    def obtive_resposta(self):
        p = ('Ok', 'Entendi', 'Certo', 'Entendido', 'Registrado')
        return random.choice(p)
    
    @property
    def obtive_nao(self):
        p = ('Ok', 'Entendi', 'Certo')
        return random.choice(p)
    
    @property
    def causa_ja_existe(self):
        p = ('Uma informação referente à essa parada ja foi registrada',
            'Já encontrei registros desse horário', 'A causa dessa parada ja foi registrada')
        c = ('deseja substituir esse registro?', 'deseja registrar novamente?',
            'deseja refazer o registro?', 'deseja fazer um novo registro?')
        r = random.choice(p) + ', ' + random.choice(c)
        return r

# Instance Object
chat = ChatTurno()

##########################################################################################################################

# Get Timestamp
def timestamp():
    return datetime.datetime.now()

# Get Turno from
def get_turno(hour: int):
    if hour < 8: return 0
    if hour < 16: return 8
    if hour < 24: return 16

# Get-Turma
def get_turma(
    date: str = None,
    turno: Literal[0, 8, 16] = None
):
    ts = timestamp()
    if date == None: date = ts.strftime('')
    if turno == None: turno = get_turno(ts.hour)
    return  ['A','B','C','D'][0]

##########################################################################################################################