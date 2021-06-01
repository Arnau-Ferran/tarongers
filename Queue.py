
class Queue:
    empaquetador = None
    size = None
    # TODO enlaces: atr's i metodes.
    # TODO estadistics

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.state = "empty"
        self.size = 0
        # inicialitzar estadistics

    def tractar_esdeveniment(self, event):
        if event.type == 'END_TRANSPORT':
            #if self.state != "empty":
            print("Queue got END_TRANSPORT and it is on "+self.state)
            #else:
            self.processar_end_transport(event)

        elif event.type == 'END_EMPAQUETAMENT':
            if self.state != "notempty":
                print("Queue got END_TRANSPORT but it is on empty")
            else:
                self.processar_end_transport(event)

    def processar_end_transport(self, event):
        if self.empaquetador.getState == "idle":
            #li passo al empaquetador el min entre les q li falten i les q li puc passar.
            self.empaquetador.arribenTaronges(min(50 - self.empaquetador.getSize), event.numTaronges)       # nose si el max i min funcionen. i en general aixo es pot fer mes bonic
            #després de passar endevant totes les q puc, les q queden se'm sumen. son o 0 o les q m'ha arribat - les q he passat endavant.
            self.size = self.size + max(0, event.numTaronges-(50 - self.empaquetador.getSize))
            if self.size == 0:
                self.state="empty"
            else:
                self.state ="notempty"
        else:
            self.size = self.size + event.numTaronges
            self.state = "notempty"
