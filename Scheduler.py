from Empaquetador import Empaquetador
from Recollector import Recollector
from Queue import Queue
from Server import *
from Source import *
from Event import *


class Scheduler:
    currentTime = 0
    eventList = []
    ntreballadors = 0
    sources = []
    servers = []
    recollectors = []
    tempsFiSimulacio=432000

    def __init__(self):
        # creació dels objectes que composen el meu model

        self.sources = []
        self.servers = []
        # inicialitztem cadascuna de les hectàrees (processors i generadors d'entitats)
        for x in range(0, 5):
            server = Server(self)
            source = Source(self)
            self.servers.append(server)
            self.sources.append(source)

        '''for server in self.servers:
                server.crearConnexio(server2,queue) #TODO no sé molt bé què he de fer'''

        # self.Queue = Queue()   #monty

        i = 0
        for source in self.sources:
            source.crearConnexio(self.servers[i])  # TODO no sé molt bé què he de fer
            i = i + 1

        self.queue = Queue(self)
        #per ara un sol empaquetador
        self.empaquetador = Empaquetador(self, 0)
        self.queue.crearConnexioAmbEmpaquetador(self.empaquetador)
        self.empaquetador.crearConnexioAmbQueue(self.queue)

        self.simulationStart = Event(self, 'SIMULATION_START', 0, None)
        self.eventlist = []
        self.eventList.append(self.simulationStart)

    def run(self):
        # configurar el model per consola, arxiu de text...
        self.configurarModel()

        # rellotge de simulacio a 0
        self.currentTime = 0

        eventIterator = 0

        # bucle de simulació (condició fi simulació llista buida)
        # while self.eventList[eventIterator]:
        while self.currentTime<self.tempsFiSimulacio and Iterator < len(self.eventList) :
            print("Esdeveniment número:" + str(eventIterator))
            # recuperem event simulacio
            event = self.eventList[eventIterator]
            # actualitzem el rellotge de simulacio
            self.currentTime = event.time
            if self.currentTime<self.tempsFiSimulacio:
                # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
                # també podríem delegar l'acció a un altre objecte
                event.object.tractarEsdeveniment(event)
                eventIterator = eventIterator + 1
        # recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)

    def tractarEsdeveniment(self, event):
        if (event.type == "SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se
            print('Entro a tractar esdeveniment al scheduler')
            for i in range(0, 5):
                self.sources[i].tractarEsdeveniment(event)
                self.servers[i].tractarEsdeveniment(event)

    def configurarModel(self):
        print("Introdueix el nombre de treballadors recol·lectors al camp de tarongers, entre 5 i 10 : ")
        num = int(input())
        while (num < 5 or num > 10):
            print("Torna a introduïr un nombre vàlid de treballadors: ")
            num = int(input())
        ntreballadors = num

        for x in range(0, ntreballadors-1):
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
        for r in self.recollectors:
            r.recollirEstadistics()
        self.queue.recollirEstadistics()
        self.empaquetador.recollirEstadistics()



if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
