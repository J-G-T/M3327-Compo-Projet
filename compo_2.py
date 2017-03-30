from pyo import *
import random
from Resources.Graverb import Graverb
from Resources.PRead import PRead
from Resources.AutoR import AutoR

s = Server().boot()

'''
Compo_3: AutoMusic 

Une musique se compose « seul », algorithmiquement, a l'aide de trois sons. 

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
    sound1 = "Sound/g3_megflute.wav"
    sound2 = "Sound/g3_aeros.wav"
    sound3 = "Sound/g3_ring.wav"

env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])

ptr1 = PRead(sound1, spd=7, min=0.4, max=0.42, mul=0.7)
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