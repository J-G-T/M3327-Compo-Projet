#!/usr/bin/env python
# encoding: utf-8

from pyo import *
import random
from Resources.DM import DM
from Resources.OscAug import OscAug

#DEVELOPPEMENT #
s = Server(winhost='asio').boot()
s.setStartOffset(60)

#Table pour OscAug#
tab = CurveTable(list=[(0, 0), (250, 0.1), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                   (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])
                                   
tab2 = CurveTable(list=[(0, 0), (250, 0.7), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                     (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])

tab3 = CurveTable(list=[(0, 0), (250, 0.1), (500, 0.15), (1000, 0.2), (1500, 0.3), (2000, 0.4), (3000, 0.5), 
                                     (4096, 0.8), (5000, 0.5), (6100, 0.375), (7000, 0.2), (8191, 0.0)])
#Table pour Rythme
tabd = CurveTable(list=[(0,0.7), (1024, 0.3), (2048, 0.3), (4096, 0.8), (6144, 0.05), (8192, 0)])

###################
##SECTION OBJET AUDIO##
###################

#Graves
autog1 = Sine(0.1).range(0.1, 0.20)
autog2 = Sine(0.05).range(0.15, 0.22)
og = OscAug(tab, phs=.05, ofrq=50, dur=93, mul=autog1)
og2 = OscAug(tab, phs=.01, ofrq=101, dur=85, mul=autog2)
og3 = OscAug(tab3, phs=.07, allfeed=.05, ofrq=51, dur=101, mul=0.27).out()

#Melo
om = OscAug(tab2, phs=0.28, ofrq=midiToHz(53), allfeed=10, dur=4.5, mul=0.25)
om2 = OscAug(tab2, phs=0.35, ofrq=midiToHz(56), allfeed=8, dur=4.5, mul=0.25)
om.sFade(1.2, 2.3); om2.sFade(1.2, 2.3)

#Rythme principal.
autdrm = Sine(0.09).range(0, 0.5)
autof1 =Sine(40).range(20, 1000)
drm = DM(tabd, ffrq=1000, f1=0, f2=1, of=autof1, mul=autdrm)
#Rthm B.
autdrb = Sine(.5).range(250, 400)
autof2 =Sine(40).range(20, 120)
drb = DM(tabd, ffrq=autdrb, f1=0, f2=0, of=autof2, mul=0.7)
drbverb = WGVerb(drb.sig(), feedback=0.8, bal=0.3).out()

#Rythm cymb.
autof3 = Sine(30).range(200, 2000)
dcmb = DM(tabd, ffrq=350, f1=1, f2=3, of=autof3, mul=0.3)
rcfad = Fader(fadein=0.1, fadeout=0.1, dur=0.1001)
filtest1 = Tone(dcmb.sig(), freq=4500, mul=rcfad).out()

#Rythm final.
autof4 = Sine(40).range(20, 80)
dmf = DM(tabd, ffrq=500, f1=0, f2=0, q=1, of=autof4, feedback=0.67, bal=0.35, mul=1.2)


################
#GESTION DES EVENTS#
################

list = [53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75]
count = 0
cf = 0
prate = 0
lastind = 7
z = 6
x = 6

def drum():
    drm.play()

def dbass():
    drb.play()

def dcymb():
    dcmb.splay()
    rcfad.play()

def final():
    global cf
    if cf == 40:
        patf.stop()
    elif cf % 10 == 0:
        pass
    elif cf % 4 != 0:
        dmf.play()
    elif cf % 4 == 0:
        dcmb.play()
    cf += 1

def melo():
    global count, prate, lastnote, lastind, z, x
    prate += 1
    if prate <= 5:
        if count == 0:
            om.out()
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
            om2.out()
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

def event_0():
    pass
def event_1():
    pass
def event_2():
    og.out()
    btdb.play()
def event_3():
    patr.play()
def event_4():
    btcmb.play()
    og2.out()
def event_5():
    btdb.stop()
def event_6():
    btdb.play()
def event_7():
    drm.sFeedb(0.75)
def event_8():
    btcmb.stop()
    patr.stop()
def event_9():
    btcmb.play()
    btdb.play()
def event_10():
    pass
def event_11():
    drm.sFeedb(0.8)
    patr.play()
def event_12():
    btdb.stop()
    btcmb.stop()
def event_13():
    pass
def event_14():
    drm.sFeedb(0.95)
    patr.stop()
    btcmb.play()
def event_15():
    btdb.play()
def event_16():
    pass
def event_17():
    btcmb.stop()
def event_18():
    pass
def event_19():
    btcmb.play()
def event_20():
    drm.sFeedb(0.65)
    patr.play()
    btcmb.stop()
def event_21():
    pass
def event_22():
    btcmb.play()
def event_23():
    pass
def event_24():
    patm.stop()
    patr.stop()
    btdb.stop()
    btcmb.stop()
    patf.play()
def event_25():
    pass
def event_26():
    m.stop()
def event_27():
    pass

    
##############
#SECTION PATTERN#
##############

#Pattern de la pi�ce
m = Metro(4).play()
c = Counter(m, min=0, max=26)
sc = Score(c)

#Trig pour melo
patm = Pattern(function=melo, time=2).play()

#Trig Drum Principal
patr = Pattern(function=drum, time=0.125)

#Trig Drum Bass
btdb = Beat(time=.125, taps=16, w1=70, w2=50, w3=35)
patb = TrigFunc(btdb, function=dbass)

#Trig Drum Cymb.
btcmb = Beat(time=.125, taps=16, w1=10, w2=20, w3=25)
patc = TrigFunc(btcmb, function=dcymb)

#Trig Drum Final.
patf = Pattern(final, time=.125)



s.gui(locals())