from pyo import *
import random

s = Server().boot()
s.setStartOffset(30)

sfp = SfPlayer('vert.wav', speed=1, loop=True)
f_len = sndinfo('vert.wav')[1]


#PHASE VOCODER SECTION
pa = PVAnal(sfp, size=2048, overlaps=8, wintype=2)
pb = PVBuffer(pa,index=Sine(0.1, mul=0.35, add=0.35), length=f_len)
ps = PVSynth(pb)


#EFFECTS
verb = WGVerb(ps, feedback=0.7, cutoff=10000, bal=0.6).out()


s.gui(locals())