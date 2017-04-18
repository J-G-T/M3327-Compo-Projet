#!/usr/bin/env python
# encoding: utf-8

from pyo import *
from Resources.Graverb import Graverb
from Resources.PRead import PRead
from Resources.AutoR import AutoR

s = Server(winhost="asio", buffersize=512).boot()

'''
Compo_3: AutoMusic 
    Une musique se compose « seul », algorithmiquement, a l'aide de trois sons. 
    L'evolution temporelle se divise comme suit: 
        Sound1 -> Deconstruction -> Sound2 -> Deconstruction -> Sound3 -> Finale. 


Note:
    -Rajouter des loops de random pour un meilleur controle au sein de la piece (voir ex table_05)
        
    -Essayer d'optimiser le tout!
        - Import Time sur les class pour avoir un stop doux sur 0.1 seconde? -> Smoother les transitions.

'''

GSOUND = 1

if GSOUND == 0:
    sound1 = 'Sound/mota.wav'
    sound2 = 'Sound/motb.wav'
    sound3 = 'Sound/motc.wav'
elif GSOUND == 1:
    sound1 = 'Sound/vert.wav'
    sound2 = 'Sound/vertflute.wav'
    sound3 = 'Sound/vertintf.wav'
elif GSOUND == 2:
    sound1 = 'Sound/motb.wav'
    sound2 = 'Sound/vertflute.wav'
    sound3 = 'Sound/hypergong.wav'
 
env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])
env2 = CosTable(list=[(0,0.3), (2000, 0.1), (2500,0.7), (4600, 0.45), (8192,0.0000)])

##################
##GESTION DES SONS###
#################

#SfPlayer pour son original.
sfad1 = Fader(fadein=0.1, fadeout=8, dur=28, mul=0.65)
sfad2 = Fader(fadein=6, fadeout=5, dur=24, mul=0.65)
sfad3 = Fader(fadein=7, fadeout=6, dur=18, mul=0.95)

sf1 = SfPlayer(sound1, loop=True, mul=sfad1).out()
sf2 = SfPlayer(sound2, loop=True, mul=sfad2)
sf3 = SfPlayer(sound3, loop=True, mul=sfad3)

#Particule impulsive.
ar1 = AutoR(sound1, env, time=0.2, dur=0.2, dens=200, ftt=1, filfrq=5000, mul=0.25)

ar2 = AutoR(sound2, env, time=0.15, dur=0.15, dens=220, ftt=0, filfrq=4500, mul=0.35)
ar2.setFadInOut(0.05, 0.1)

ar3 = AutoR(sound3, env, time=0.5, dur=0.5, dens=200, ftt=2, filfrq=5000, mul=0.25)
ar3.setFadInOut(0.25, 0.25)

#Grain avec Reverb, son de duree moyenne.
pr1 = PRead(sound1, spd=0.0001, type=2, mul=0.6)
pr2 = PRead(sound2, spd=0.5, type=1, mul=0.6)
pr3 = PRead(sound3, spd=0.45, type=1, mul=0.8)

grav1 = Fader(fadein=0.05, fadeout=0.05, dur=0.2, mul=1.2)
grv1 = Graverb(pr1.sig(), env2, time=0.5, dur=0.2, fb=0.8, type=0, bal=0.6, mul=grav1)

grav2 = Fader(fadein=0.2, fadeout=0.3, dur=0.5, mul=1)
grv2 = Graverb(pr2.sig(), env, time=0.5, dur=0.5, fb=0.7, type=0, bal=0.4, mul=grav2)

grav3 = Fader(fadein=0.5, fadeout=1.3, dur=2, mul=1)
grv3 = Graverb(pr3.sig(), env2, time=2, dur=2, fb=0.8, type=0, bal=0.7, mul=grav3)

#Trames sonores.
adr1 = AutoR(sound1, env, time=10, dur=10, dens=200, ftt=0, filfrq=4000, mul=0.3)
adr1.setFadInOut(5, 5)

adr2 = AutoR(sound2, env2, time=5, dur=5, dens=400, ftt=1, filfrq=2000, mul=0.5)
adr2.setFadInOut(3, 2)

adr3 = AutoR(sound3, env, time=7, dur=7, dens=350, ftt=0, filfrq=1500, mul=0.4)
adr3.setFadInOut(5, 2)


compts = Compress(adr1.sig()+adr2.sig()+adr3.sig(), thresh=-30, ratio=3)

#Deconstruction total
prand1 = PRead(sound1, spd=0.10, min=0.1, max=0.55, type=3, mul=0.15)
prand2 = PRead(sound2, spd=0.15, min=0.05, max=0.2, type=3, mul=0.15)
prand3 = PRead(sound3, spd=0.25, min=0.5, max=0.8, type=3, mul=0.15)


####################
#GESTION DES EVENEMENTS#
###################

#EVENEMENT A DECLENCHER PENDANT LA PIECE#
#PARTICULE
def parti1():
    ar1.play()
def parti2():
    ar2.play()
def parti3():
    ar3.play()
#GRAIN REVERB
def graverb1():
    grav1.play()
def graverb2():
    grav2.play()
def graverb3():
    grav3.play()
#TRAMES
def trame1():
    adr1.play()
def trame2():
    adr2.play()
def trame3():
    adr3.play()


####################

def event_0():
    sfad1.play() 
def event_1():
    pass
def event_2():
    ar3.out(); pi3.play()
def event_3():
    grv1.out(); pg1.play()
def event_4():
    ar2.out(); pi2.play()
    grv2.out(); pg2.play()
    ar3.stop(); pi3.stop()
def event_5():
    grv3.out(); pg3.play()
    ar1.out(); pi1.play()
def event_6():
    compts.out()
    ar3.out(); pi3.play()
    adr1.out(); pt1.play()
def event_7():
    sf1.stop()
    ar2.stop(); pi2.stop()
def event_8():
    adr2.out(); pt2.play()
def event_9():
    ar3.stop(); pi3.stop()
    grv1.stop(); pg1.stop()
def event_10():
    #Sound2 -> Mid-Piece
    sf2.out(); sfad2.play()
    grv3.out(); pg3.play()
def event_11():
    grv2.stop(); pg2.stop()
    adr1.stop(); pt1.stop()
    adr2.stop(); pt2.stop()
def event_12():
    ar1.stop(); pi1.stop()
def event_13():
    adr3.out(); pt3.play()
def event_14():
    pass
def event_15():
    ar2.setTime(0.1); ar2.setDur(0.1); ar2.setDens(100); ar2.setType(0); ar2.setFadInOut(0.05, 0.05)
    pi2.time=0.1
    ar2.out(); pi2.play()
def event_16():
    sf2.stop()
    grv3.stop(); pg3.stop()
def event_17():
    pass
def event_18():
    ar1.setTime(1); ar1.setDur(1); ar1.setDens(50); ar1.setType(2)
    pi1.time=1
    ar1.out(); pi1.play()
    adr2.out(); pt2.play()
def event_19():
    pass
def event_20():
     prand1.out()
def event_21():
    pass
def event_22():
    pass
def event_23():
    prand2.out()
    ar3.setTime(2); ar3.setDur(2); ar3.setDens(80); ar3.setFilfrq(100); ar3.setType(2); ar3.setFadInOut(0.05, 0.8)
    pi3.time=2
def event_24():
    ar3.out(); pi3.play()
    grv3.out(); pg3.play()
def event_25():
    sf3.out(); sfad3.play()
def event_26():
    prand1.stop()
def event_27():
    prand3.out()
def event_28():
    pass
def event_29():
    prand1.out()
def event_30():
    pass
def event_31():
    sf3.stop()


#Pattern general
pi1 = Pattern(parti1, time=0.2)
pi2 = Pattern(parti2, time=0.15)
pi3 = Pattern(parti3, time=0.5)

pg1 = Pattern(graverb1, time=0.2)
pg2 = Pattern(graverb2, time=0.5)
pg3 = Pattern(graverb3, time=1)

pt1 = Pattern(trame1, time=10)
pt2 = Pattern(trame2, time=4)
pt3 = Pattern(trame3, time=6)

#Pattern de la piece
m = Metro(5).play()
c = Counter(m, min=0, max=31)
sc = Score(c)

s.gui(locals())