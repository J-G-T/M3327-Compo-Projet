#!/usr/bin/env python
# encoding: utf-8

from pyo import *

class Graverb:
    '''
    Granulation avec Reverb.
    
    Arguments:
        Input : PyoObject
            Input en entree de l'effet.
        env : PyoTableObject
            Enveloppe du grain.
        time : PyoObject ou Float
            Temps entre chaque grain.
        dur : PyoObject ou Float
            Duree de chaque grain.
        fb : PyoObject ou Float
            Feedback de la reverb.
        Type : float
            Type de filtre applique sur le grain.
        bal : PyoObject ou Float
            Balance entre dry/wet du son original vs avec effet.
        mul : float ou PyoObject
            Controle du volume de l'objet.

    '''
    def __init__(self, input, env, time=1, dur=0.15, fb=0.8, type=0, bal=0.5, mul=1):
        self.input = input
        #Metronome
        self.met = Metro(time=time).play()
        #Enveloppe
        self.trigenv = TrigEnv(self.met, table=env, dur=dur)
        #Random pour freq.
        self.frqf = TrigRand(self.met, min=500, max=2000, port=0.05)
        #Filt Biquadx
        self.filt = Biquadx(self.input, freq=self.frqf, type=type, stages=5, mul=self.trigenv)
        #Reverb
        self.verb = WGVerb(self.filt, feedback=fb, cutoff=5000, bal=bal, mul=mul)

    def stop(self):
        "Arret du son."
        self.verb.stop()
        return self
        
    def setTime(self, x):
        "Gestion du parametre time."
        self.met.time = x
        
    def setDur(self, x):
        "Gestion du parametre de duree."
        self.trigenv.dur = x
        
    def setFb(self, x):
        "Gestion du parametre de feedback."
        self.verb.feedback = x

    def setType(self, x):
        "Gestion du type de filtre."
        self.filt.type = x

    def setBal(self, x):
        "Gestion du parametre de balance."
        self.verb.bal = x

    def out(self, chnl=0):
        "Signal audio en sortie."
        self.verb.out(chnl)
        return self
    
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.verb
        
#SECTION TEST#
if __name__ == "__main__":

    TEST = 2

    audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
    audioServer.start()    

    env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])

    if TEST == 1:
        lfo = LFO(freq=440, sharp=0.25, type=2, mul=1)
        grv = Graverb(lfo, env, type=2, mul=0.5).out()
        
    elif TEST == 2:
        lfo = LFO(freq=440, sharp=0.3, type=0, mul=1)
        grv1 = Graverb(lfo, env, time=0.5, mul=0.1).out()
        grv2 = Graverb(lfo, env, time=0.3, mul=0.1).out()
        grv3 = Graverb(lfo, env, time=0.7, mul=0.1).out()
        
    audioServer.gui(locals())