
#millor treballar amb define o algun sistema simular a l'enum de C++
#from enumeracions import *
from Server import *
import numpy as np
import random
#from scipy.stats import triang

class Source:
    server = None
    entitatsCreades = 0
    def __init__(self, scheduler):
        # inicialitzar element de simulació
        entitatsCreades = 0
        self.scheduler = scheduler

    def crearConnexio(self, server):
        self.server = server

    def tractarEsdeveniment(self, event):
        if (event.type == 'SIMULATION_START'):
            self.simulationStart(event)

        if (event.type == 'NOVA_MADURACIO'):
            self.processNextArrival(event)

    def simulationStart(self, event):
        nouEvent = self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)
        self.state = "idle"

    def processNextArrival(self, event):
        # Cal crear l'entitat 

        #entitat=self.crearEntitat(self)
        # Mirar si es pot transferir a on pertoqui
        #transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
        #server.recullEntitat(event.time,entitat)
        self.server.novaMaduracio(event.time)

        # Cal programar la següent arribada
        nouEvent = self.properaArribada(event.time)
        self.scheduler.afegirEsdeveniment(nouEvent)

    '''def crearEntitat(self) {
        self.server.madurarTaronja(self)
    }'''

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = self.calcularTempsEntreArribades()
        # incrementem estadistics si s'escau
        self.entitatsCreades = self.entitatsCreades + 1
        #self.state = "busy"
        # programació primera arribada
        return Event(self, 'NOVA_MADURACIO', time + tempsEntreArribades, None)

    def calcularTempsEntreArribades(self):
        #random.triangular(low, high, mode)¶ Return a random floating point number N such that low <= N <= high and with the specified mode between those bounds.
        #The low and high bounds default to zero and one. The mode argument defaults to the midpoint between the bounds, giving a symmetric distribution.
        ## import numpy
        num = random.triangular(-5, 5, 0) #TODO canviar nums
        return num


