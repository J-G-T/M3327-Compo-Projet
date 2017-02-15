from pyo import *
import random

'''
Note:
    1. Essayer de rendre tous les sons mono. a l'interieur du programme... sinon les rendre mono.

'''


s = Server().boot()
#s.setStartOffset(30)

#Morceau de piece
f1 = "vert.wav"
f1_len = sndinfo('vert.wav')[1]

f2 = "vertflute.wav"
f2_len = sndinfo('vertflute.wav')[1]

f3 = "vertintf.wav"
f3_len = sndinfo('vertintf.wav')[1]
#

class BBP:
    '''
    Barberpole

    Arguments:
        input : PyoObject
            Objet pyo en entree.
        sf : float ou PyoObject
            Frequence du Sine() qui balaie le pitch
        rmin : float ou PyoObject
            Range minimum du Sine()
        rmax : float ou PyoObject
            Range maximum du Sine()
        mul : float ou PyoObject
    
    '''
    def __init__(self, input, sf=.1, rmin=-10, rmax=10, mul=1):
        self.fade = Fader(fadein=2, fadeout=2, mul=mul)
        self.pva = PVAnal(input, size=2048, overlaps=8)
        self.lfo = Sine(sf).range(rmin, rmax)
        self.pvsh = PVShift(self.pva, shift=self.lfo)
        self.pvs = PVSynth(self.pvsh)
        self.pan = Pan(self.pvs, outs=2, pan=0.5, spread=0.3, mul=self.fade)
    
    def play(self, chnl=0):
        "Retourne le signal audio en sortie de la classe"
        self.pan.out(chnl)
        self.fade.play()
        return self
        
    def stop(self):
        self.fade.stop()
        return self

sfp = SfPlayer(f2, loop=True)
pa = Pan(sfp, outs=1, pan=0.5, spread=0).out()

barb = BBP(sfp, mul=1)

def event_0():
    sfp.out()
def event_1():
    barb.play()
def event_2():
    barb.stop()
def event_3():
    barb.play()
def event_4():
    barb.stop()
    
met = Metro(5).play()
count = Counter(met, min=0, max=20)
time = Score(count)

s.gui(locals())