
class Queue:
    empaquetador = None
    size = None

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.state = "empty"
        self.size = 0
        # inicialitzar estadistics
        self.sumaTarongesOutput = 0

    def crearConnexioAmbEmpaquetador(self, nou_empaquetador):
        self.empaquetador = nou_empaquetador

    def tractar_esdeveniment(self, event):
        #when arriba una nova taronja
        if event.type == 'END_TRANSPORT':
            #if self.state != "empty":
            print("Queue got END_TRANSPORT and it is on "+self.state)
            #else:
            self.processarEndTransport(event)

        #when l'empaquetador acaba
        elif event.type == 'END_EMPAQUETAMENT':
            print("Queue got END_EMPAQUETAMENT and it is on "+self.state)
            self.processarEndEmpaquetament(event)

    def processarEndTransport(self, event):
        #si li puc passar directament a l'empaquetador
        if self.empaquetador.getState == "idle":
            #li passo al empaquetador el min entre les q li falten i les q li puc passar.
            n_taronges_passo = min((50 - self.empaquetador.getSize), event.numTaronges)       # nose si el max i min funcionen. i en general aixo es pot fer mes bonic
            self.empaquetador.arribenTaronges(n_taronges_passo)

            #estadístics
            self.sumaTarongesOutput = self.sumaTarongesOutput + n_taronges_passo

            #després de passar endevant totes les q puc, les que queden se'm sumen. son o 0 o les q m'ha arribat - les q he passat endavant.
            self.size = self.size + max(0, event.numTaronges-(50 - self.empaquetador.getSize))
            if self.size == 0:
                self.state="empty"
            else:
                self.state ="notempty"
        else:
            self.size = self.size + event.numTaronges
            self.state = "notempty"

    def processarEndEmpaquetament(self, event):
        n_taronges_passo = min(50, self.size)

        self.empaquetador.arribenTaronges(n_taronges_passo)    #ojo!! he fet aixo aqui.

        #estadístics
        self.sumaTarongesOutput = self.sumaTarongesOutput + n_taronges_passo

        self.size = max(0, self.size-50)

        if self.size == 0:
            self.state = "empty"
        else:
            self.state = "notempty"

    def getState(self):
        return self.state