#!/usr/bin/env python
# encoding: utf-8

from pyo import *

class PRead:
    '''
    Lecteur de son via objet Pointer2 et SndTable.
    
    Arguments:
        Input : PyoObject
            Input en entree de l'effet.
        spd : PyoObject ou Float        
            Vitesse de lecture de la table / Vitesse de pige de valeur au hasard
        min : PyoObject ou Float 
            Point de depart de la lecture du son, de 0 a 1 ou 0 est le debut du 0 et 1 sa fin. / Minimum de la valeur pigee.
        max : PyoObject ou Float 
            Point final de la lecture du son. / Maximum de la valeur pigee.
        type : Float
            Choix du type de lecteur pour l'objet Pointer2 (0:Sine, 1:Phasor)
        mul : float ou PyoObject
            Controle du volume de l'objet.

    '''
    def __init__(self, input, spd=0.7, min=0.66, max=0.8, type=0, mul=0.5):
        #Input
        self.input = input
        #Longueur du son
        self.length = sndinfo(self.input)[1]
        #SndTable
        self.sndtable = SndTable(self.input, start=0, stop=self.length)
        #Valeur de spd en SIG pour controle
        self.spd = Sig(spd)
        #Gestion de valeur Type
        self.type = Sig(type)
        #Initialisation du controle de l'index
        if type == 0:
            self.ind = Sine(self.spd).range(min, max)
        elif type == 1:
            self.ind = Phasor(self.spd/self.length)
        elif type == 2:
            self.chaos = ChenLee(pitch=spd, chaos=0.5, stereo=False, mul=mul)
            self.ind = Scale(self.chaos, inmin=-1, inmax=1, outmin=0, outmax=1)
        elif type == 3:
            self.time = Metro(time=spd).play()
            self.ind = TrigRand(self.time, min=min, max=max, port=0.03)
        #Pointer pour lire la table selon l'index choisi
        self.point = Pointer2(self.sndtable, self.ind, mul=mul)

    def out(self, chnl=0):
        "Signal audio en sortie"
        self.point.out(chnl)
        return self

    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.point

    def setSpd(self, x):
        "Change la valeur de la vitesse de lecture du son"
        self.spd.value = x

    def stop(self):
        "Arrete la sequence jouee"
        self.point.stop()
        return self


#SECTION TEST#
if __name__ == "__main__":

    TEST = 3

    audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
    audioServer.start()    

    sound = 'mota.wav'

    if TEST == 0:
        pr = PRead(sound, spd=0.00001, type=2, mul=0.3).out()
    elif TEST == 1:
        pr2 = PRead(sound, spd=7, min=0.4, max=0.42, mul=0.3).out()
    elif TEST == 2:
        autspd = Sine(0.1).range(0.4, 3.4)
        pr3 = PRead(sound, spd=autspd, min=0, max=1, type=1, mul=0.3).out()
    elif TEST == 3:
        autspd = Sine(0.1).range(0.1, 0.45)
        pr4 = PRead(sound, spd=autspd, min=0, max=0.2, type=1, mul=0.3).out()
        
    audioServer.gui(locals())