from pyo import *
import random
from DM import DM
        
#Generator/Class#
class OscAug:
    '''
    L'Oscillateur Augmente
    
    Oscillateur + AllPassWaveguide
    
    Arguments:
        table : PyoTableObject
            Table de forme d'onde pour l'objet Osc.
        phs : PyoObject ou float
            Controle la vitesse de changement de phase de l'objet Osc.
        ofrq : float ou PyoObject
            Frequence de l'oscillateur
        allfrq : float ou PyoObject
            Frequence de resonance du filtre waveguide allpass.
        allfeed : float ou PyoObject
            Controle la vitesse de variation du feedback du allpass.
        dur : float
            Durée de l'enveloppe. 
        mul : float ou PyoObject
            Controle du volume de l'instrument.

    '''
    def __init__(self, table, phs=.1, ofrq=45, allfrq=50, allfeed=.01, dur=0, mul=0.5):
        #Fader pour gerer les clicks.
        self.fade = Fader(fadein=1, fadeout=1.5, dur=dur, mul=mul)
        #Automation
        self.oaut = Sine(freq=phs, mul=0.5, add=0.5)
        self.allaut = Sine(freq=allfeed, mul=0.25, add=0.75)
        self.daut = Sine(freq=.1, mul=0.005, add=0.010)
        #SigTo - Pour gerer les changements de frequences
        self.freq = SigTo(value=ofrq, time=0.005, init=ofrq)
        #Oscillateur avec table 
        self.osc = Osc(tab, freq=self.freq, phase=self.oaut, mul=0.15)
        #AllPass applique a Osc.
        self.alw = AllpassWG(self.osc.mix(2), freq=allfrq, feed=self.allaut, detune=0.21)
        #Compression du signal avant l'envoi.
        self.comp = Compress(self.alw, thresh=-10, ratio=10, mul=self.fade)
        #Delai court/reverb pour rajouter de la couleur.
        self.dela = Delay(self.comp, delay=self.daut, mul=self.fade)
        self.dverb = WGVerb(self.dela, feedback=0.95, cutoff=1800, bal=0.8, mul=mul)
        #Objs.
        self.objs = self.comp + self.dela + self.dverb

    def out(self, chnl=0):
        "Retourne le signal audio en sortie de la classe"
        self.objs.out(chnl)
        self.fade.play()
        return self

    def stop(self):
        self.fade.stop()
        return self

    def play(self):
        self.fade.play()
        return self

    def setofrq(self, x):
        "Change la frequence de l'oscillateur"
        self.freq.value = x

    def playm(self, x):
        self.freq.value = midiToHz(x)
        self.fade.play()

#SECTION DE TEST#
s = Server().boot()

#Table(s)#
tab = CurveTable(list=[(0, 0), (250, 0.1), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                   (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])
tab2 = CurveTable(list=[(0, 0), (250, 0.7), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                     (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])
#tab.view()
#tab2.view()

tabd = CurveTable(list=[(0,0.7), (1024, 0.3), (2048, 0.3), (4096, 0.8), (6144, 0.05), (8192, 0)])
tabd.view()


#Graves
og = OscAug(tab, phs=.05, ofrq=50).out()
og2 = OscAug(tab, phs=.01, ofrq=100, mul=0.3).out()

#Aigue
oa = OscAug(tab, phs=0.05, ofrq=4000, allfeed=1, mul=0.05, dur=0.5).out()

#Melo
om = OscAug(tab2, phs=0.28, ofrq=midiToHz(53), allfeed=10, dur=3).out()
om2 = OscAug(tab2, phs=0.34, ofrq=midiToHz(56), allfeed=8, dur=3).out()
om.stop(); om2.stop()

#Rythme
autdm = Sine(0.1).range(0, 0.6)
drm = DM(tabd, ffrq=1000, f1=0, f2=1, mul=autdm).play()


#Gestion du temps#
ptime = 0
count = 0
prate = 0

def melo():
    global count, prate, ptime
    prate += 1
    if prate <= 5:
        if count == 0:
            #Pige note pour om;
            om.playm(random.choice([53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 74]))
            count += 1
        elif count == 1:
            
            om2.playm(random.choice([53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 74]))
            count -= 1
    elif prate > 7 and prate < 10:
        om.stop(); om2.stop()
    elif prate >= 10:
        prate -= 10

def drum():
    drm.play()

pat = Pattern(function=[melo], time=2).play()
patr = Pattern(function=drum, time=0.125).play()
s.gui(locals())