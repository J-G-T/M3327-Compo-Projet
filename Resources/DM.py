#!/usr/bin/env python
# encoding: utf-8

from pyo import *
import random

class DM:
    '''
    Drum Machine
    
    Arguments:
        table : PyoTableObject
            Table de forme d'onde pour l'objet Osc.
        ffrq : float ou PyoObject
            Frequence des deux filtres (au choix).
        f1 : float
            Choix du filtre 1 selon l'objet biquad.
        f2 : float
            Choix du filtre 2 selon l'objet biquad.
        q : float
            Q des filtres.
        feedback : float ou PyoObject
            Feedback de la reverb.
        bal : float ou PyoObject
            Balance entre wet/dry du signal de reverb.

    '''
    def __init__(self, table, ffrq=500, f1=0, f2=1, q=2, of=1000, feedback=0.6, bal=0.3, mul=1):
        self.fadn = Fader(fadein=0.001, fadeout=0.1, dur=0.1001, mul=mul)
        self.osc = Osc(table, freq=of).mix(2)
        self.nos = Noise(mul=self.fadn)
        self.filt1 = Biquad(self.nos*self.osc, freq=ffrq, q=q, type=f1)
        self.filt2 = Biquad(self.filt1, freq=ffrq, q=q, type=f2)
        self.dverb = WGVerb(self.filt1+self.filt2, feedback=feedback, bal=bal)

    def play(self):
        self.fadn.play()
        self.dverb.out()
        return self

    def splay(self):
        self.fadn.play()
        return self

    def stop(self):
        self.fadn.stop()
        self.dverb.stop()

    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.dverb

    def sFeedb(self, x):
        "Change la valeur de feedback de la reverb"
        self.dverb.feedback = x
        
    def sMul(self, x):
        "Change la valeur du volume."
        self.fadn.mul = x
        
    def tail(self):
        self.fadn.stop()
        self.osc.stop()

#SECTION TEST#
if __name__ == "__main__":

    TEST = 0

    audioServer = Server(sr=44100, nchnls=2, buffersize=256, winhost='asio').boot()
    audioServer.start()

    tabd = CurveTable(list=[(0,0.7), (1024, 0.3), (2048, 0.3), (4096, 0.8), (6144, 0.05), (8192, 0)])
    

    if TEST == 0:
        autof = Sine(40).range(20, 800)
        drm = DM(tabd, ffrq=1000, f1=0, f2=1, of=autof).play()
        def drum():
            drm.play()
        patty = Pattern(drum, time=0.5).play()

    elif TEST == 1:
        drm = DM(tabd, ffrq=1000, f1=1, f2=3)
        fade1 = Fader(fadein=0.1, fadeout=0.1, dur=0.1001)
        filtest1 = Tone(drm.sig(), freq=3000, mul=fade1)
        vreb1 = Freeverb(filtest1, size=0.3, damp=0.8, bal=0.45).out()
        
        def drum():
            drm.splay()
            fade1.play()
        patty = Pattern(drum, time=1).play()

    elif TEST == 2:
        drm = DM(tabd, ffrq=1000, f1=0, f2=1, feedback=0.85)
        def drum():
            drm.play()
        def event_0():
            pass
        def event_1():
            drm.sFeedb(0.95)
            drm.tail()
            
        m = Metro(2).play()
        c = Counter(m, min=0, max=2)
        sc = Score(c)

        patty = Pattern(drum, time=0.125).play()

    audioServer.gui(locals())