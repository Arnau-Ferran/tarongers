from Server import *
import numpy as np
import random


class Recollector:
    my_id = None
    queue = None
    # servers = []
    # estadistics:
    n_taronges_recollides = None

    def __init__(self, scheduler, recollector_id):
        self.scheduler = scheduler
        # self.servers = []
        self.state = "idle"
        self.my_id = recollector_id
        # TODO: enllaçar el queue
        # inicialitzar estadistics:
        n_taronges_recollides = 0  # todo incrementar

    def tractar_esdeveniment(self, event):
        if event.type == 'END_TRANSPORT':
            if self.state != "busy":
                print("Recollector " + self.my_id + " got END_TRANSPORT but it is on idle")
            else:
                self.processar_end_transport(event)
        else:
            if event.type == 'DONE_RECOLLINT':
                if self.state != "busy":
                    print("Recollector " + self.my_id + " got DONE_RECOLLINT but it is on idle")
                    self.processarDoneRecollint(event)

    def assignarRecollector(self, server, time):
        if self.state != "idle":
            print("Recollector " + self.my_id + " got ASSIGNAR_RECOLLECTOR but it is on busy")

        t_caminar = 90  # TODO
        event_arribo = Event(server, 'RECOLLECTOR_ARRIBA', time + t_caminar, None)
        self.scheduler.afegirEsdeveniment(event_arribo)

        self.state = "busy"

    def processar_end_transport(self, event):
        self.state = "idle"

    def processarDoneRecollint(self, event):
        t_transportar = 500  # TODO

        event_transportar = Event(self, 'END_TRANSPORT', event.time + t_transportar, None)
        self.scheduler.afegirEsdeveniment(event_transportar)

        event_transportar_queue = Event(self.queue, 'END_TRANSPORT', event.time + t_transportar, None)
        self.scheduler.afegirEsdeveniment(event_transportar_queue)

        self.state = "busy"

    def get_state(self):
        return self.state
