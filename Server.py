
# millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import * #monty

from Server import *
from Event import *


class Server:
    treballadors = []
    recoAssignat = None
    def __init__(self, scheduler):
        # inicialitzar element de simulació
        entitatsTractades=0
        #entitatsPendents = 0
        self.state="empty"
        self.scheduler=scheduler
        self.entitatActiva=None
        nTarongesPerRecollir = 0
        
    def crearConnexio(self,recollectors):
        self.treballadors = recollectors

    
    def novaMaduracio(self,time):
        #self.entitatsTractades=entitat
        self.programarRecullida(time)


    def tractarEsdeveniment(self,event):
        if (event.type == 'SIMULATION_START'):
            self.simulationStart(event)
        if(event.type == "RECOLLECTOR_ARRIBA"):
            self.arribaRecollector(event)
        if(event.type == "DONE_RECOLLINT"):
            self.recollectorAcaba(event)
        if (event.type == 'END_SERVICE'):
            self.processarFiServei(event)

    def simulationStart(self, event):
        self.state = "idle"
        self.entitatsTractades = 0
        self.entitatsPendents=0

    def arribaRecollector(self,event):
        t_recolleccio = self.calcularTempsRecolleccio()
        nouEvent = Event(self, 'DONE_RECOLLINT', event.time + t_recolleccio, None)
        eventArecollector = Event(self.recoAssignat, 'DONE_RECOLLINT', event.time + t_recolleccio, None)
        self.scheduler.afegirEsdeveniment(nouEvent)
        self.scheduler.afegirEsdeveniment(eventArecollector)
        self.state == "collecting"

    def recollectorAcaba(self):
        self.state = "empty"
        self.recoAssignat = None

    def calcularTempsRecolleccio(self):
        return 15 #TODO posar distro

    def programarRecollida(self, time):

        # incrementem estadistics si s'escau
        self.entitatsTractades = self.entitatsTractades + 1
        self.nTarongesPerRecollir = self.nTarongesPerRecollir + 1
        if (recoAssignat is None):
            for t in self.treballadors:
                if (t.getState() == "idle" ):
                    t.assignarRecollector(self,time)
                    self.recoAssignat = t

            self.state = "readyToCollect"



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
