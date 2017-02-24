from pyo import *

audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
audioServer.start()

class OscAug:
    '''
    L'Oscillateur Augmente
    
    Oscillateur + AllPassWaveguide
    
    Arguments:
        table : PyoTableObject
            Table de forme d'onde pour l'objet Osc.
        phs : PyoObject ou float
            Controle la vitesse de changement de phase de l'objet Osc.
        ofrq : float ou PyoObject
            Frequence de l'oscillateur
        allfeed : float ou PyoObject
            Controle la vitesse de variation du feedback du allpass.
        dur : float
            Duree de l'enveloppe ; Doit duree au moins 3.5 Secondes.
        mul : float ou PyoObject
            Controle du volume de l'instrument.

    '''
    def __init__(self, table, phs=.1, ofrq=45, allfeed=.01, dur=0, mul=0.5):
        #Fader pour gerer les clicks.
        self.fade = Fader(fadein=1, fadeout=1, dur=dur, mul=mul)
        #Automation
        self.oaut = Sine(freq=phs, mul=0.5, add=0.5)
        self.allaut = Sine(freq=allfeed, mul=0.25, add=0.75)
        self.daut = Sine(freq=.1, mul=0.005, add=0.010)
        #SigTo - Pour gerer les changements de frequences
        self.freq = SigTo(value=ofrq, time=0.005, init=ofrq)
        #Oscillateur avec table 
        self.osc = Osc(tab, freq=self.freq, phase=self.oaut, mul=0.15)
        #AllPass applique a Osc.
        self.alw = AllpassWG(self.osc.mix(2), freq=50, feed=self.allaut, detune=0.21)
        #Compression du signal avant l'envoi.
        self.comp = Compress(self.alw, thresh=-10, ratio=10, mul=self.fade)
        #Delai court/reverb pour rajouter de la couleur.
        self.dela = Delay(self.comp, delay=self.daut, mul=self.fade)
        self.dverb = WGVerb(self.dela, feedback=0.95, cutoff=1800, bal=0.8, mul=mul)
        #Objs.
        self.objs = self.comp + self.dela + self.dverb

    def out(self, chnl=0):
        "Out basique pour objet de type trame"
        self.objs.out(chnl)
        self.fade.play()
        return self

    def stop(self):
        "Methode pour arreter la sortie audio"
        self.fade.stop()
        return self

    def play(self):
        "Play pour objet qui necessite des changements d'amplitudes rapides"
        self.fade.play()
        return self

    def setofrq(self, x):
        "Change la frequence de l'oscillateur"
        self.freq.value = x

    def playm(self, x):
        "Choix de note selon 12 <= x <= 127 (MIDI)"
        self.freq.value = midiToHz(x)
        self.fade.play()
        
    def sFade(self, x, y):
        "Ajustement du fadein et fadeout"
        self.fade.fadein = x
        self.fade.fadeout = y
        
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.objs

#SECTION TEST#

tab = CurveTable(list=[(0, 0), (250, 0.1), (500, 0.25), (1000, 0.075), (1500, 0.1), (2000, 0.7), (3000, 0.7), 
                                   (4096, 0.3), (5000, 0.1), (6100, 0.15), (7000, 0.1), (8191, 0.0)])

if __name__ == "__main__":
    OA1 = OscAug(tab, mul=0.6).out()
    OA2 = OscAug(tab, phs=0.75, ofrq=500, dur=5, mul=0.2).out()
    def Osc():
        OA2.play()

    patty = Pattern(Osc, time=5).play()
    
    audioServer.gui(locals())