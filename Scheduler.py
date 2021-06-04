from Empaquetador import Empaquetador
from Recollector import Recollector
from Queue import Queue
from Server import *
from Source import *
from Event import *
from sortedcontainers import SortedDict


class Scheduler:
    currentTime = 0
    #eventList = []
    eventDict = SortedDict()
    ntreballadors = 0
    sources = []
    servers = []
    recollectors = []
    tempsFiSimulacio=604800
    enableTraces = True

    def __init__(self):
        self.enableTraces = True

        # creació dels objectes que composen el meu model

        self.sources = []
        self.servers = []
        # inicialitztem cadascuna de les hectàrees (processors i generadors d'entitats)
        for x in range(0, 6):
            server = Server(self, x)
            source = Source(self, x)
            self.servers.append(server)
            self.sources.append(source)

        i = 0
        for source in self.sources:
            source.crearConnexio(self.servers[i])
            i = i + 1

        self.queue = Queue(self)
        #per ara un sol empaquetador
        self.empaquetador = Empaquetador(self, 0)
        self.queue.crearConnexioAmbEmpaquetador(self.empaquetador)
        self.empaquetador.crearConnexioAmbQueue(self.queue)

        self.simulationStart = Event(self, 'SIMULATION_START', 0, None)
        self.eventlist = []
        self.eventDict[0] = self.simulationStart

    def sortTime(self, event):
        return event.time


    def run(self):
        # configurar el model per consola, arxiu de text...
        self.configurarModel()

        # rellotge de simulacio a 0
        self.currentTime = 0

        eventIterator = 0

        # bucle de simulació (condició fi simulació llista buida)
        while self.currentTime<self.tempsFiSimulacio and eventIterator < len(self.eventDict):
            #print("Esdeveniment número:" + str(eventIterator))

            # recuperem event simulacio
            event = self.eventDict.peekitem(index=eventIterator)[1]
            # actualitzem el rellotge de simulacio
            self.currentTime = event.time
            #print("currentTime = "+str(self.currentTime))
            if self.currentTime<self.tempsFiSimulacio:
                # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
                # també podríem delegar l'acció a un altre objecte
                event.object.tractarEsdeveniment(event)
                eventIterator = eventIterator + 1
        # recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada

        if self.eventDict.__contains__(event.time): #si dona la casualitat que el temps és repetit, tornem a intentar amb un nombre negligiblement diferent
            event.time += 0.0000001
            self.afegirEsdeveniment(event)
        else:
            self.eventDict[event.time] = event

    def tractarEsdeveniment(self, event):
        if (event.type == "SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se
            #print('Entro a tractar esdeveniment al scheduler')
            for i in range(0, 6):
                self.sources[i].tractarEsdeveniment(event)
                self.servers[i].tractarEsdeveniment(event)

    def configurarModel(self):
        print("Introdueix el nombre de treballadors recol·lectors al camp de tarongers, entre 5 i 10 : ")
        num = int(input())
        while (num < 5 or num > 10):
            print("Torna a introduïr un nombre vàlid de treballadors: ")
            num = int(input())
        ntreballadors = num

        for x in range(0, ntreballadors):
            recollector = Recollector(self, x)
            self.recollectors.append(recollector)
            recollector.crearConnexioAmbQueue(self.queue)
        for s in self.servers:
            s.crearConnexio(self.recollectors)

    def recollirEstadistics(self):
        print("A continuació us mostrarem els estadístics recollits per cadascun dels components del model: ")
        for s in self.sources:
            s.recollirEstadistics()
        for se in self.servers:
            se.recollirEstadistics()
        '''for r in self.recollectors:
            r.recollirEstadistics()'''
        self.queue.recollirEstadistics()
        self.empaquetador.recollirEstadistics()


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
