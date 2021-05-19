from Server import *
from Source import *
from Event import *;



class Scheduler:

    currentTime = 0
    eventList = []
    treballadors = 0
    
    def __init__(self):
        # creació dels objectes que composen el meu model
        
        self.source = Source()
        self.servers = []
        #inicialitztem cadascuna de les hectàrees (processors i generadors d'entitats)
        for x in range(0, 5):
            Server = Server()
            Source = Source()
            self.servers.append(Server)
            self.sources.append(Sources)

        for server in self.servers:
            server.crearConnexio(server2,queue) #TODO no sé molt bé què he de fer

        self.Queue = Queue()
        i=0
        for source in self.sources:
            self.source[i].crearConnexio(server[i])#TODO no sé molt bé què he de fer
            ++i
    
        self.simulationStart=Event(self,'SIMULATION_START', 0,null)
        self.eventlist = []
        self.eventList.append(simulationStart)

    def run(self):
        #configurar el model per consola, arxiu de text...
        self.configurarModel()


        #rellotge de simulacio a 0
        self.currentTime=0        

        eventIterator = 0
        #bucle de simulació (condició fi simulació llista buida)
        while self.eventList[eventIterator]: 
            #recuperem event simulacio
            event=self.eventList[eventIterator]
            #actualitzem el rellotge de simulacio
            self.currentTime=event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.objecte.tractarEsdeveniment(event)
            ++eventIterator
        
        #recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        self.eventList.inserirEvent(event)


    def tractarEsdeveniment(self,event):
        if (event.tipus=="SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se     
            
    '''def configurarModel(self):
        print("Indica el número de treballadors: ")
        self.treballadors= int(input())'''



            
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
