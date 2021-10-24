
##########################################################################################################################

import py_misc

##########################################################################################################################
#                                                    CLASSE LAMINADOR                                                    #
##########################################################################################################################

# Laminador Class
class Laminador:

    # Inint Laminador
    def __init__(self, misc: py_misc):
        # Reference Miscellaneous
        self.misc = misc
        # Instance Mill
        self.quente = self.Gen(self.misc)
        self.frio = self.Gen(self.misc)
        
    # General Methods for Lam
    class Gen:

        def __init__(self, misc: py_misc):
            # Allow info inside Turno
            self.misc = misc
    
        # Relatorio Producao
        def prod(self):
            return None
        
        # Relatorio Producao do Mes
        def prod_mes(self):
            return None
        
        # Relatorio Turno
        def turno(self):
            return None

##########################################################################################################################
