#!/usr/bin/env python
# encoding: utf-8

from pyo import *

class AutoR:
    '''
    Auto Reader ; Lecture aleatoire d'un son en granulation avec choix sur le hasard.
    
    Arguments:
        Input : PyoObject
            Input en entree de l'effet.
        env : PyoTableObject
            Enveloppe du grain.
        time : PyoObject ou Float
            Temps entre chaque grain.
        dur : PyoObject ou Float
            Duree du fader interne.
        dens : PyoObject ou Float
            Densitee de grain par seconde.
        filfrq : PyoObject ou Float
            Filtre des grains.
        ftt : Float
            Choix du type du filtre sur les grains.
        mul : float ou PyoObject
            Controle du volume de l'objet.

    '''
    def __init__(self, input, env, time=1, dur=0.15, dens=100, filfrq=18000, ftt=2, mul=0.1):
        #Input
        self.input = input
        #Fader
        self.fad = Fader(fadein=0.05, fadeout=0.1, dur=dur, mul=mul)
        #Longueur(1)/SampleRate(2) du son
        self.snd = sndinfo(self.input)
        #SndTable
        self.soundtable = SndTable(self.input, start=0, stop=self.snd[1])
        #Metro/Trig
        self.met = Metro(time=time).play()
        #Automatisation de la position
        self.random = TrigRand(self.met, min=1, max=self.snd[2]*self.snd[1], port=0.01)
        #Particle2 pour la position
        self.parti = Particle2(self.soundtable, env, dens=dens, pitch=1, pos=self.random, filterfreq=filfrq, filtertype=ftt,
                                        mul=self.fad)        

    def play(self):
        "Action du fader en marche"
        self.fad.play()
        return self

    def stop(self):
        "Arret du son."
        self.parti.stop()
        return self
        
    def setTime(self, x):
        "Gestion du temps"
        self.met.time = x
        
    def setDur(self, x):
        "Gestion de la duree du fader"
        self.fad.dur = x
        
    def setDens(self, x):
        "Gestion de la densite du grain"
        self.parti.dens = x
        
    def setFilfrq(self, x):
        "Gestion de la frequence du filtre interne"
        self.parti.filterfreq = x
        
    def setType(self, x):
        "Gestion du type de filtre interne"
        self.parti.filtertype = x
        
    def setFadInOut(self, x, y):
        "Gestion du Fadein et Fadeout"
        self.fad.fadein = x
        self.fad.fadeout = y
        
    def setMul(self, x):
        "Gestion du volume"
        self.fad.mul = x

    def out(self, chnl=0):
        "Signal audio en sortie."
        self.parti.out(chnl)
        return self
        
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.parti
        
#SECTION TEST#
if __name__ == "__main__":

    TEST = 2

    audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
    audioServer.start()    

    env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])
    sound = 'vertflute.wav'

    if TEST == 1:
        autr = AutoR(sound, env, time=0.125, dens=250, filfrq=2000, ftt=2, mul=0.3).out()
        
    elif TEST == 2:
        autr = AutoR(sound, env, time=1, dens=500, filfrq=15000, ftt=0, mul=0.1).out()
        
    audioServer.gui(locals())