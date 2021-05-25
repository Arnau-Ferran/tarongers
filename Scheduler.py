from Server import *
from Source import *
from Event import *


class Scheduler:
    currentTime = 0
    eventList = []
    treballadors = 0
    ntreballadors = 0
    sources = []
    servers = []

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
        #while self.eventList[eventIterator]:
        while eventIterator < len(self.eventList):
            print("Esdeveniment número:" + str(eventIterator))
            # recuperem event simulacio
            event = self.eventList[eventIterator]
            # actualitzem el rellotge de simulacio
            self.currentTime = event.time
            print(str(self.currentTime))
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.object.tractarEsdeveniment(event)
            eventIterator = eventIterator + 1
        #recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)

    def tractarEsdeveniment(self, event):
        if (event.type == "SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se
            for i in range(0, 5):
                self.sources[i].tractarEsdeveniment(event)
                self.servers[i].tractarEsdeveniment(event)

            
    def configurarModel(self):
        ntreballadors = 6

    def recollirEstadistics(self):
        print("Estic recollint estadistics varis")




if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
