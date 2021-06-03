
from Server import *
from numpy import random


class Empaquetador:
    my_id = None
    #suposo
    queue = None
    size = None

    def __init__(self, scheduler, empaquetador_id):
        self.scheduler = scheduler
        self.state = "idle"
        self.my_id = empaquetador_id
        self.size = 0
        # estadistics # n_caixes_enviades és molt important => potser hauria de estar en una altra classe a lo global o algo aixi ns
        self.suma_taronges_intput = 0  #probably useless
        self.n_caixes_enviades = 0

    def crearConnexioAmbQueue(self, nou_queue):
        self.queue = nou_queue

    def arribenTaronges(self, n_taronges_arribadores, time):
        if self.state != "idle":
            print("Empaquetador " + self.my_id + " got arribenTaronges but it is on busy")
        else:
            self.size = self.size+n_taronges_arribadores

            #estadístic
            self.suma_taronges_intput = self.suma_taronges_intput + n_taronges_arribadores

            #queue ja garanteix q no em passarà més del compte
            if self.size == 50:
                t_empaquetar = random.exponential(0.5, 90)   #TODO comprovar si els nums tenen sentit. potser està al revés
                print("random.exponential(0.5, 90) returned "+ t_empaquetar)

                event_end_empaquetament = Event(self, 'END_EMPAQUETAMENT', time + t_empaquetar, None)
                self.scheduler.afegirEsdeveniment(event_end_empaquetament)

                event_end_empaquetament_queue = Event(self.queue, 'END_EMPAQUETAMENT', time + t_empaquetar, None)
                self.scheduler.afegirEsdeveniment(event_end_empaquetament_queue)

                self.state = "busy"

            #(else em quedo a idle)

    def tractar_esdeveniment(self, event):
        if event.type == 'END_EMPAQUETAMENT':
            if self.state != "busy":
                print("Empaquetador " + self.my_id + " got END_EMPAQUETAMENT but it is on idle")
            else:
                self.processarEndEmpaquetament(event)

    def processarEndEmpaquetament(self, event):
        self.n_caixes_enviades = self.n_caixes_enviades + 1

        self.size = 0

        self.state="idle"

    def recollirEstadistics(self):
        print("Empaquetador: suma taronges input: "+self.suma_taronges_intput)
        print("Empaquetador: NUMERO DE CAIXES ENVIADES: " + self.n_caixes_enviades)