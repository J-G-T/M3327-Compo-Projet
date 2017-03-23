from pyo import *
import random
from Resources.Graverb import Graverb

s = Server().boot()

'''
Compo_3: AutoMusic 

Une musique se compose « seul », algorithmiquement, a l'aide de trois sons. 

'''

GSOUND = 2

if GSOUND == 0:
    sound1 = 'Sound/mota.wav'
    sound2 = 'Sound/motb.wav'
    sound3 = 'Sound/motc.wav'
elif GSOUND == 1:
    sound1 = 'Sound/vert.wav'
    sound2 = 'Sound/vertflute.wav'
    sound3 = 'Sound/vertintf.wav'
elif GSOUND == 2:
    sound1 = "Sound/g3_megflute.wav"
    sound2 = "Sound/g3_aeros.wav"
    sound3 = "Sound/g3_ring.wav"

env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])

class PRead:
    def __init__(self, input, spd=0.7, min=0.66, max=0.8, mul=0.5):
        self.input = input
        #Longueur du son
        self.length = sndinfo(self.input)[1]
        #SndTable
        self.sndtable = SndTable(self.input, start=0, stop=self.length)
        #Initialisation du contrôle de l'index
        self.ind = Sine(spd).range(min, max)
        #Pointer pour lire la table selon l'index
        self.point = Pointer2(self.sndtable, self.ind, mul=mul)

    def out(self, chnl=0):
        "Signal audio en sortie"
        self.point.out(chnl)
        return self

    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.point

class AutoR:
    def __init__(self, input, env, time=1, dens=100, filfrq=18000, ftt=2, mul=0.1):
        self.input = input
        #Longueur du son
        self.length = sndinfo(self.input)[1]
        #SampleRate du son
        self.sprate = sndinfo(self.input)[2]
        #SndTable
        self.soundtable = SndTable(self.input, start=0, stop=self.length)
        #Metro/Trig
        self.met = Metro(time=time).play()
        #Automatisation de la position
        self.random = TrigRand(self.met, min=1, max=self.sprate*self.length, port=0.05)
        #Particle2 pour la position
        self.parti = Particle2(self.soundtable, env, dens=dens, pitch=1, pos=self.random, filterfreq=filfrq, filtertype=ftt,
                                        mul=mul)

    def out(self, chnl=0):
        "Signal audio en sortie"
        self.parti.out(chnl)
        return self
        
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.parti

ptr1 = PRead(sound1, spd=0.1, mul=0.7)
ptr2 = PRead(sound2, spd=0.4, min=0.15, max=0.4, mul=0.3)
ptr3 = PRead(sound3, spd=5, min=0.2, max=0.6, mul=0.05)

grav1 = Graverb(ptr1.sig(), env, time=2, dur=0.05, fb=0.9, bal=0.6, mul=1).out()
grav2 = Graverb(ptr2.sig(), env, time=0.15, dur=0.15, fb=0.7, bal=0.8, mul=1).out()
grav3 = Graverb(ptr3.sig(), env, dur=0.2, fb=0.9, bal=0.86, mul=1).out()

autar1 = Sine(.1, phase=0.75).range(0, 0.05)

ar1 = AutoR(sound1, env, dens=500, time=10, ftt=0, filfrq=2000, mul=autar1).out()
ar2 = AutoR(sound2, env).out()
ar3 = AutoR(sound3, env, time=0.125, dens=300, filfrq=1000).out()

#Passer un compressor au bout de tout les sons pour gérer les sons trop puissant

s.gui(locals())