from py_wapp import Bot

##########################################################################################################################
#                                                    CLASSE LAMINADOR                                                    #
##########################################################################################################################

# Laminador Class
class Laminador:

    def __init__(self, bot: Bot):
        self.misc = bot.misc
        
        # General Methods for Lam
        class Gen:

            def __init__(self):
                # Allow info inside Turno
                self.misc = bot.misc

            # Relatorio Producao
            def prod(self):
                return None

            # Relatorio Producao do Mes
            def prod_mes(self):
                return None

            # Relatorio Turno
            def turno(self):
                return None

        self.quente = Gen()
        self.frio = Gen()

# Instance Class
Lam = Laminador()