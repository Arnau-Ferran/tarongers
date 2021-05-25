#millor treballar amb define o algun sistema simular a l'enum de C++
#from enumeracions import *
from Server import *
#from scipy.stats import triang

class Source:

    def __init__(self,scheduler):
        # inicialitzar element de simulació
        entitatsCreades=0
        self.state=idle
        self.scheduler=scheduler
    
    def crearConnexio(self,server):
        self.server=server     

    def tractarEsdeveniment(self, event):
        if (event.tipus=='SIMULATION START'):
            self.simulationStart(event)

        if (event.tipus=='NEXT ARRIVAL'):
            self.processNextArrival()
  

    def simulationStart(self,event):
        nouEvent=self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self,event):
        # Cal crear l'entitat 
        #entitat=self.crearEntitat(self)
        # Mirar si es pot transferir a on pertoqui
        #transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
        #server.recullEntitat(event.time,entitat)
        server.recullEntitat(event.time)
        # Cal programar la següent arribada
        nouEvent=self.properaArribada(event.temps)
        self.scheduler.afegirEsdeveniment(nouEvent)

    '''def crearEntitat(self) {
        self.server.madurarTaronja(self)
    }'''

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = self.calcularTempsEntreArribades()
        # incrementem estadistics si s'escau
        self.entitatsCreades=self.entitatsCreades+1
        self.state = busy
        # programació primera arribada
        return Event(self,'NEXT ARRIVAL', time+ tempsEntreArribades,null)   

    def calcularTempsEntreArribades(self,event):
        #return tempsEntreArribades() #implementar distribució del inter-arrival time dels sources triangular(129.0, 167.0, 148.0, getstream(current))
        return 15
         