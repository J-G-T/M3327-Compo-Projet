from pyo import *
import random
from Resources.DM import DM
from Resources.OscAug import OscAug

#DEVELOPPEMENT #
s = Server().boot()
s.amp = 0.6

#Table pour OscAug#
tab = CurveTable(list=[(0, 0), (250, 0.1), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                   (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])
tab2 = CurveTable(list=[(0, 0), (250, 0.7), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                     (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])
#Table pour Rythme
tabd = CurveTable(list=[(0,0.7), (1024, 0.3), (2048, 0.3), (4096, 0.8), (6144, 0.05), (8192, 0)])

##SECTION OBJET AUDIO##
#Graves
og = OscAug(tab, phs=.05, ofrq=50).out()
og2 = OscAug(tab, phs=.01, ofrq=100, mul=0.3).out()

#Aigue
oa = OscAug(tab, phs=0.1, ofrq=4200, allfeed=1, mul=0.05, dur=2).out()

#Melo
om = OscAug(tab2, phs=0.28, ofrq=midiToHz(53), allfeed=10, dur=4.5, mul=0.35).out()
om2 = OscAug(tab2, phs=0.35, ofrq=midiToHz(56), allfeed=8, dur=4.5, mul=0.35).out()
om.sFade(1.2, 2.3); om2.sFade(1.2, 2.3)
om.stop(); om2.stop()

#Rythme principal.
autdm = Sine(0.1).range(0, 0.5)
drm = DM(tabd, ffrq=1000, f1=0, f2=1, mul=autdm).play()
#Rthm B.
autdrb = Sine(.5).range(250, 400)
drb = DM(tabd, ffrq=autdrb, f1=0, f2=0, mul=0.7).play()
drbverb = WGVerb(drb.sig(), feedback=0.8, bal=0.3).out()
#Rythm cymb.
dcmb = DM(tabd, ffrq=350, f1=1, f2=3, mul=0.10).play()


#GESTION DU TEMPS#
count = 0
prate = 0
lastind = 7
z = 6
x = 6
list = [53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75]

def melo():
    global count, prate, lastnote, lastind, z, x
    prate += 1
    if prate <= 5:
        if count == 0:
            #Pige note selon list (Fa min) pour om;
            if lastind > 1 and lastind < 12:
                z = random.randint(-2, 2) + lastind
                note = list[z]
                om.playm(note)
                lastind = z
            elif lastind <= 1:
                z = random.randint(2, 5) + lastind
                note = list[z]
                om.playm(note)
                lastind = z
            elif lastind >= 12:
                z = random.randint(-5, -2) + lastind
                note = list[z]
                om.playm(note)
                lastind = z
            count += 1
        elif count == 1:
            #Pige note selon list (Fa min) pour om2;
            if lastind > 1 and lastind < 12:
                x = random.randint(-2, 2) + lastind
                note = list[x]
                om2.playm(note)
                lastind = x
            elif lastind <= 1:
                x = random.randint(2, 5) + lastind
                note = list[x]
                om2.playm(note)
                lastind = x                
            elif lastind >= 12:
                x = random.randint(-5, -2) + lastind
                note = list[x]
                om2.playm(note)
                lastind = x
            count -= 1
    elif prate > 7 and prate < 10:
        om.stop(); om2.stop()
    elif prate >= 10:
        prate -= 10


def drum():
    drm.play()

def dbass():
    drb.play()
    
def dcymb():
    dcmb.play()

pat = Pattern(function=[melo], time=2).play()
patr = Pattern(function=drum, time=0.125).play()

#Trig Drum Bass
btdb = Beat(time=.125, taps=16, w1=40, w2=50, w3=35).play()
patb = TrigFunc(btdb, function=dbass).play()

#Trig Drum Cymb.
btcmb = Beat(time=.125, taps=16, w1=10, w2=20, w3=25).play()
patc = TrigFunc(btcmb, function=dcymb).play()

s.gui(locals())