from pyo import *
import random

s = Server().boot()

TEST = 0

if TEST == 0:
    sound1 = 'mota.wav'
    sound2 = 'motb.wav'
    sound3 = 'motc.wav'
elif TEST == 1:
    sound1 = 'vert.wav'
    sound2 = 'vertflute.wav'
    sound3 = 'vertintf.wav'

env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])

class Graverb:
    def __init__(self, input, env, time=1, dur=0.15, fb=0.8, bal=0.5, mul=0.3):
        self.input = input
        #Metronome
        self.met = Metro(time=time).play()
        #Enveloppe
        self.trigenv = TrigEnv(self.met, table=env, dur=dur)
        #Random pour freq.
        self.frqf = TrigRand(self.met, min=500, max=2000, port=0.05)
        #Filt Biquadx
        self.filt = Biquadx(self.input, freq=self.frqf, mul=self.trigenv)
        #Reverb
        self.verb = WGVerb(self.filt, feedback=fb, cutoff=5000, bal=bal, mul=mul)
        
    def out(self, chnl=0):
        "Signal audio en sortie."
        self.verb.out(chnl)
        return self
    
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.verb
   
class PRead:
    def __init__(self, input, spd=0.7, min=0.66, max=0.8, mul=0.5):
        self.input = input
        #Longueur du son
        self.lenght = sndinfo(self.input)[1]
        #Table qui lit le son en input
        self.sndtable = SndTable(self.input, start=0, stop=self.lenght)
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

ptr1 = PRead(sound1, mul=0.7)
ptr2 = PRead(sound2, spd=0.4, min=0.15, max=0.4, mul=0.3)
ptr3 = PRead(sound3, spd=5, min=0.2, max=0.6, mul=0.05)

grav1 = Graverb(ptr1.sig(), env, time=0.05, dur=0.05, fb=0.7, bal=0.6, mul=1).out()
grav2 = Graverb(ptr2.sig(), env, time=0.15, dur=0.15, fb=0.7, bal=0.8, mul=1).out()
grav3 = Graverb(ptr3.sig(), env, dur=0.2, fb=0.7, bal=0.66, mul=1).out()


s.gui(locals())