#Main Start

from pyo import *
s = Server().boot()

#AUDIO#
sf1 = SfPlayer('mb_1.wav', speed=0.10, loop=True)
sf2 = SfPlayer('mb_4.wav', speed=0.5, loop=True)

#PITCH TRACKERs#
pittra1 = Yin(sf1, minfreq=20, maxfreq=10000)
pittra2 = Yin(sf2, minfreq=20, maxfreq=10000)

#RANDOMIZERS#
aut1 = Sine(freq=0.5, mul=2, add=pittra1*2)
aut2 = Sine(freq=0.5, mul=5, add=pittra2)

#GENERATORS
genosc1 = RCOsc(pittra1, mul=0.05)
genosc2 = RCOsc(aut1, mul=0.05)
genosc3 = RCOsc(aut2, mul=0.05).mix(2)

#EFFECT FOR GENOSC1#
rev1 = Freeverb(genosc1, size=0.4, damp=0.6, bal=0.25)

#EFFECT FOR GENOSC3#
rev3 = Freeverb(genosc3, size=0.4, damp=0.6, bal=0.55)
del3 = Delay(rev3, delay=0.5, feedback=0.25, mul=0.5)
filt3 = Biquad(del3+rev3, freq=300, q=1, type=1).out()
spec = Spectrum(filt3)


s.gui(locals())

