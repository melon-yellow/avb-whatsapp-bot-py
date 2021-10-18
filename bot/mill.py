##########################################################################################################################
#                                                    CLASSE LAMINADOR                                                    #
##########################################################################################################################

# Laminador Class
class Laminador:

    def __init__(self):
        # General Methods for Lam
        class Gen:

            def __init__(self):
                # Allow info inside Turno
                self.misc = Avbot.misc

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