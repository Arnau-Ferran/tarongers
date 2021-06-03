
class Queue:
    empaquetador = None
    size = None
    # estadistics:
    sumaTarongesOutput = None

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.state = "empty"
        self.size = 0
        # inicialitzar estadistics:
        self.sumaTarongesOutput = 0

    def crearConnexioAmbEmpaquetador(self, nou_empaquetador):
        self.empaquetador = nou_empaquetador

    def tractar_esdeveniment(self, event):
        #when arriba una nova taronja
        if event.type == 'END_TRANSPORT':
            self.processarEndTransport(event)

        #when l'empaquetador acaba
        elif event.type == 'END_EMPAQUETAMENT':
            if self.state != "notempty":
                print("Queue got END_EMPAQUETAMENT and it is on empty. it's not an error but it's useless")
            else:
                self.processarEndEmpaquetament(event)

    def processarEndTransport(self, event):
        #si li puc passar directament a l'empaquetador
        if self.empaquetador.getState == "idle":    #aixo implica que la cua està buida
            #li passo al empaquetador el min entre les q li falten i les q li puc passar.
            n_taronges_passo = min((50 - self.empaquetador.getSize), event.numTaronges)       # nose si el max i min funcionen. i en general aixo es pot fer mes bonic
            self.empaquetador.arribenTaronges(n_taronges_passo, event.time)

            #estadístics
            self.sumaTarongesOutput = self.sumaTarongesOutput + n_taronges_passo

            #després de passar endevant totes les q puc, les que queden se'm sumen. son o 0 o les q m'ha arribat - les q he passat endavant.
            self.size = self.size + max(0, event.numTaronges-(50 - self.empaquetador.getSize))
            if self.size == 0:
                self.state="empty"
            else:
                self.state ="notempty"
        else:       # not empty sempre va aquí
            self.size = self.size + event.numTaronges
            self.state = "notempty"

    def processarEndEmpaquetament(self, event):
        n_taronges_passo = min(50, self.size)

        self.empaquetador.arribenTaronges(n_taronges_passo, event.time)    #ojo!! he fet aixo aqui.

        #estadístics
        self.sumaTarongesOutput = self.sumaTarongesOutput + n_taronges_passo

        self.size = max(0, self.size-50)

        if self.size == 0:
            self.state = "empty"
        else:
            self.state = "notempty"

    def getState(self):
        return self.state

    def recollirEstadistics(self):
        print("Queue: suma taronges output: "+ str(self.sumaTarongesOutput))