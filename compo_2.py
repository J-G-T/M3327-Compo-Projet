from pyo import *
import random
from Resources.Graverb import Graverb
from Resources.PRead import PRead
from Resources.AutoR import AutoR

s = Server(winhost="asio").boot()

'''
Compo_3: AutoMusic 

Une musique se compose « seul », algorithmiquement, a l'aide de trois sons. 

Note:
    -Rajouter des loops de random pour un meilleur controle au sein de la piece (voir ex table_05)
    
'''

GSOUND = 3

if GSOUND == 0:
    sound1 = 'Sound/mota.wav'
    sound2 = 'Sound/motb.wav'
    sound3 = 'Sound/motc.wav'
elif GSOUND == 1:
    sound1 = 'Sound/vert.wav'
    sound2 = 'Sound/vertflute.wav'
    sound3 = 'Sound/vertintf.wav'
elif GSOUND == 2:
    sound1 = 'Sound/hypergong.wav'
    sound2 = 'Sound/g3_aeros.wav'
    sound3 = 'Sound/g3_ring.wav'
elif GSOUND == 3:
    sound1 = 'Sound/motb.wav'
    sound2 = 'Sound/vertflute.wav'
    sound3 = 'Sound/hypergong.wav'
 
env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])

##################
##GESTION DES SONS##
#################

#DEBUT#
sfad = Fader(fadein=0.1, fadeout=8, dur=28, mul=0.65)
sf = SfPlayer(sound1, loop=True, mul=sfad).out()

#TRANSITION DEBUT/DEVELOPPEMENT#
#Apparition de particule de son depuis AutoR sur les trois sons.
fad1 = Fader(fadein=0.10, fadeout=0.05, dur=0.2, mul=0.10)
ar1 = AutoR(sound1, env, time=0.2, dens=230, ftt=1, filfrq=5000, mul=fad1).out()

fad2 = Fader(fadein=0.05, fadeout=0.05, dur=0.10, mul=0.2)
ar2 = AutoR(sound2, env, time=0.15, dens=240, ftt=0, filfrq=4500, mul=fad2).out()

fad3 = Fader(fadein=0.3, fadeout=0.1, dur=0.5, mul=0.33)
ar3 = AutoR(sound3, env, time=0.5, dens=500, ftt=2, filfrq=5000, mul=fad3).out()

#DEVELOPPEMENT
#Particule avec Reverb legerement plus long / Disparition de son original.
pr1 = PRead(sound1, spd=0.0001, type=2, mul=0.5)
pr2 = PRead(sound2, spd=0.5, type=1, mul=0.5)
pr3 = PRead(sound3, spd=0.5, type=0, mul=0.8)

frav1 = Fader(fadein=0.1, fadeout=0.1, dur=0.2, mul=1.5)
grv1 = Graverb(pr1.sig(), env, time=0.5, dur=0.2, fb=0.8, type=0, bal=0.6, mul=frav1).out()

frav2 = Fader(fadein=0.3, fadeout=0.1, dur=0.5, mul=1.25)
grv2 = Graverb(pr2.sig(), env, time=0.5, dur=0.5, fb=0.7, type=0, bal=0.4, mul=frav2).out()

frav3 = Fader(fadein=0.5, fadeout=0.5, dur=2, mul=1.5)
grv3 = Graverb(pr3.sig(), env, time=2, dur=2, fb=0.9, type=2, bal=0.7, mul=frav3).out()

#Apparition de trames sonores.
fadr1 = Fader(fadein=5, fadeout=5, dur=10, mul=0.35)
adr1 = AutoR(sound1, env, time=10, dens=300, ftt=0, filfrq=4000, mul=fadr1)

fadr2 = Fader(fadein=2, fadeout=2, dur=4, mul=0.55)
adr2 = AutoR(sound2, env, time=4, dens=500, ftt=1, filfrq=2000, mul=fadr2)

compts = Compress(adr1.sig()+adr2.sig(), thresh=-30, ratio=2).out()

#EVENEMENT A DECLENCHER PENDANT LA PIECE#
#IMPULSION
def impul1():
    fad1.play()
def impul2():
    fad2.play()
def impul3():
    fad3.play()
#GRAIN REVERB
def grav1():
    frav1.play()
def grav2():
    frav2.play()
def grav3():
    frav3.play()
#TRAMES
def trame1():
    fadr1.play()
def trame2():
    fadr2.play()


####################

def event_0():
    sfad.play()
def event_1():
    pass
def event_2():
    pi3.play()
def event_3():
    pg1.play()
def event_4():
    pi2.play()
    pi3.stop()
    pi1.play()
    pg2.play()
def event_5():
    pg3.play()
def event_6():
    pi3.play()
    pt1.play()
    sf.stop()
def event_7():
    pass
def event_8():
    pt2.play()
    pi2.stop()
def event_9():
    pi3.stop()
    pg1.stop()
def event_10():
    pass
def event_11():
    pass
def event_12():
    pass
def event_13():
    pass
def event_14():
    pass
def event_15():
    pass
def event_16():
    pass
def event_17():
    pass


#Pattern general
pi1 = Pattern(impul1, time=0.15)
pi2 = Pattern(impul2, time=0.15)
pi3 = Pattern(impul3, time=0.15)

pg1 = Pattern(grav1, time=0.2)
pg2 = Pattern(grav2, time=0.5)
pg3 = Pattern(grav3, time=2)

pt1 = Pattern(trame1, time=10)
pt2 = Pattern(trame2, time=4)
#pt3 = Pattern(trame3, time=2)

#Pattern de la piece
m = Metro(5).play()
c = Counter(m, min=0, max=15)
sc = Score(c)

s.gui(locals())