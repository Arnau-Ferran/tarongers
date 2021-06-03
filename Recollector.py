from Server import *


class Recollector:
    my_id = None
    queue = None
    #no necessita enllaç amb servers.
    # estadistics:
    n_taronges_recollides_i_transportades = None

    def __init__(self, scheduler, recollector_id):
        self.scheduler = scheduler
        self.state = "idle"
        self.my_id = recollector_id
        # inicialitzar estadistics:
        self.n_taronges_recollides_i_transportades = 0

    def crearConnexioAmbQueue(self, nou_queue):
        self.queue = nou_queue

    def assignarRecollector(self, server, time):
        if self.state != "idle":
            print("Recollector " + self.my_id + " got ASSIGNAR_RECOLLECTOR but it is on busy")

        else:
            t_caminar = 90  # TODO
            event_arribo = Event(server, 'RECOLLECTOR_ARRIBA', time + t_caminar, None)
            self.scheduler.afegirEsdeveniment(event_arribo)

            self.state = "busy"

    def tractarEsdeveniment(self, event):
        if event.type == 'END_TRANSPORT':
            if self.state != "busy":
                print("Recollector " + self.my_id + " got END_TRANSPORT but it is on idle")
            else:
                self.processar_end_transport(event)
        else:
            if event.type == 'DONE_RECOLLINT':
                if self.state != "busy":
                    print("Recollector " + str(self.my_id) + " got DONE_RECOLLINT but it is on idle")
                else:
                    self.processarDoneRecollint(event)

    def processar_end_transport(self, event):
        #actualitzar estadistics
        self.n_taronges_recollides_i_transportades += event.numTaronges
        self.state = "idle"

    def processarDoneRecollint(self, event):
        t_transportar = 300  # TODO

        event_transportar = Event(self, 'END_TRANSPORT', event.time + t_transportar, event.numTaronges)
        self.scheduler.afegirEsdeveniment(event_transportar)

        event_transportar_queue = Event(self.queue, 'END_TRANSPORT', event.time + t_transportar, event.numTaronges)
        self.scheduler.afegirEsdeveniment(event_transportar_queue)

        self.state = "busy"

    def getState(self):
        return self.state

    def recollirEstadistics(self):
        print("Recollector "+ str(self.my_id) +": num de taronges recollides i transportades: "+ str(self.n_taronges_recollides_i_transportades))
