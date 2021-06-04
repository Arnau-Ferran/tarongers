
# millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import * #monty

from Server import *
from Event import *
from numpy import random


class Server:
    treballadors = []
    recoAssignat = None
    def __init__(self, scheduler, id):
        # inicialitzar element de simulació
        self.entitatsTractades=0
        #entitatsPendents = 0
        self.state="empty"
        self.scheduler=scheduler
        self.entitatActiva=None
        self.nTarongesPerRecollir = 0
        self.my_id = id
        self.entitatsSortida = 0
        
    def crearConnexio(self,recollectors):
        self.treballadors = recollectors

    
    def novaMaduracio(self,time):
        #self.entitatsTractades=entitat
        self.programarRecollida(time)


    def tractarEsdeveniment(self,event):
        if event.type == 'SIMULATION_START':
            self.simulationStart(event)
        if event.type == "RECOLLECTOR_ARRIBA":
            self.arribaRecollector(event)
        if event.type == "DONE_RECOLLINT":
            self.recollectorAcaba()


    def simulationStart(self, event):
        self.state = "idle"
        self.entitatsTractades = 0
        self.entitatsPendents=0

    def arribaRecollector(self,event):
        #traces
        if self.scheduler.enableTraces:
            print("Arriba un Recollector al Server "+str(self.my_id)+".\nRecollint taronges... (Server "+str(self.my_id)+")")

        t_recolleccio = self.calcularTempsRecolleccio()
        nouEvent = Event(self, 'DONE_RECOLLINT', event.time + t_recolleccio, self.nTarongesPerRecollir)
        eventArecollector = Event(self.recoAssignat, 'DONE_RECOLLINT', event.time + t_recolleccio, self.nTarongesPerRecollir)
        self.scheduler.afegirEsdeveniment(nouEvent)
        self.scheduler.afegirEsdeveniment(eventArecollector)
        self.state = "collecting"

    def recollectorAcaba(self):
        self.state = "empty"
        self.recoAssignat = None
        self.entitatsSortida += self.nTarongesPerRecollir
        self.nTarongesPerRecollir = 0

    def calcularTempsRecolleccio(self):
        tempsRecollecio = random.exponential(72,1)
        #print("random.exponential(72,10)[0] is "+ str(tempsRecollecio[0]))
        return tempsRecollecio[0]

    def programarRecollida(self, time):

        # incrementem estadistics si s'escau
        self.entitatsTractades = self.entitatsTractades + 1
        self.nTarongesPerRecollir = self.nTarongesPerRecollir + 1
        if self.recoAssignat is None:
            i = 0
            found = False
            while i<len(self.treballadors) and not found:
                t = self.treballadors[i]
                if t.getState() == "idle":
                    t.assignarRecollector(self,time)
                    self.recoAssignat = t
                    found = True
                i+=1

            self.state = "readyToCollect"

    def recollirEstadistics(self):
         print("Server " + str(self.my_id) +  " Número d'entitats tractades: " + str(self.entitatsTractades) )
         print("Server " + str(self.my_id) +  " Número d'entitats que han sortit: " + str(self.entitatsSortida))


