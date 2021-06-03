
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
        print(self.treballadors.getState())

    
    def novaMaduracio(self,time):
        #self.entitatsTractades=entitat
        self.programarRecollida(time)


    def tractarEsdeveniment(self,event):
        if (event.type == 'SIMULATION_START'):
            self.simulationStart(event)
        if(event.type == "RECOLLECTOR_ARRIBA"):
            self.arribaRecollector(event)
        if(event.type == "DONE_RECOLLINT"):
            self.recollectorAcaba()


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
        self.entitatsSortida += self.nTarongesPerRecollir

    def calcularTempsRecolleccio(self):
        tempsRecollecio = random.exponential(72,10)[0] # TODO comprovar si els nums tenen sentit. potser està al revés
        #print("random.exponential(72,10) returned "+ str(tempsRecollecio))
        return tempsRecollecio

    def programarRecollida(self, time):

        # incrementem estadistics si s'escau
        self.entitatsTractades = self.entitatsTractades + 1
        self.nTarongesPerRecollir = self.nTarongesPerRecollir + 1
        if self.recoAssignat is None:
            for t in self.treballadors:
                if t.getState() == "idle":
                    t.assignarRecollector(self,time)
                    self.recoAssignat = t

            self.state = "readyToCollect"



    def recollirEstadistics(self):
         print("Server " + str(self.my_id) +  " Número d'entitats tractades: " + str(self.entitatsTractades) )
         print("Server " + str(self.my_id) +  " Número d'entitats que han sortit: " + str(self.entitatsSortida))


