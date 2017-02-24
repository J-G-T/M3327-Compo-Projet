from pyo import *
import random

audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
audioServer.start()

tabd = CurveTable(list=[(0,0.7), (1024, 0.3), (2048, 0.3), (4096, 0.8), (6144, 0.05), (8192, 0)])

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
    def __init__(self, table, ffrq=500, f1=0, f2=1, q=2, feedback=0.6, bal=0.3, mul=1):
        self.fadn = Fader(fadein=0.001, fadeout=0.1, dur=0.1001, mul=mul)
        self.osc = Osc(table, freq=1000).mix(2)
        self.nos = Noise(mul=self.fadn)
        self.filt1 = Biquad(self.nos*self.osc, freq=ffrq, q=q, type=f1)
        self.filt2 = Biquad(self.filt1, freq=ffrq, q=q, type=f2)
        self.dverb = WGVerb(self.filt1+self.filt2, feedback=feedback, bal=bal).out() 

    def play(self):
        self.fadn.play()
        return self

    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.dverb

#SECTION TEST#
if __name__ == "__main__":
    drm = DM(tabd, ffrq=1000, f1=0, f2=1).play()
    def drum():
        drm.play()

    patty = Pattern(drum, time=1).play()
    
    audioServer.gui(locals())