
# millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import * #monty

from Server import *
from Event import *


class Server:
    server = None

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        entitatsTractades=0
        self.state="idle"
        self.scheduler=scheduler
        self.entitatActiva=None
        
    def crearConnexio(self,server2,queue):
        self.queue=queue
        self.server=server2
    
    def recullEntitat(self,time):
        #self.entitatsTractades=entitat
        self.programarFinalServei(time)


    def tractarEsdeveniment(self, event):
        if (event.tipus == 'SIMULATION START'):
            self.simulationStart(event)

        if (event.tipus == 'END_SERVICE'):
            self.processarFiServei(event)

    def simulationStart(self, event):
        self.state = "idle"
        self.entitatsTractades = 0


    def programarFinalServei(self, time):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = 10
        # incrementem estadistics si s'escau
        self.entitatsTractades = self.entitatsTractades + 1
        self.state = "busy"
        # programació final servei
        return Event(self, 'END_SERVICE', time + tempsServei, entitat)

    def processarFiServei(self, event):
        # Registrar estadístics
        self.entitatsTractades = self.entitatsTractades + 1
        # Mirar si es pot transferir a on per toqui
        if (self.server.estat == "idle"):
            # transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
            self.server.recullEntitat(event.time, event.entitat)
        else:
            if (self.queue.estat == "idle"):
                self.queue.recullEntitat(event.time, event.entitat)
            # ...
        self.estat = "idle"

    # ...
