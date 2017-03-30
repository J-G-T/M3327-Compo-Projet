from pyo import *

class AutoR:
    '''
    Auto Reader ; Lecture aleatoire d'un son en granulation avec choix sur le hasard.
    
    Arguments:
        Input : PyoObject
            Input en entree de l'effet.
        env : PyoTableObject
            Enveloppe du grain.
        time : PyoObject ou Float
            Temps entre chaque grain.
        dens : PyoObject ou Float
            Densitee de grain par seconde.
        filfrq : PyoObject ou Float
            Filtre des grains.
        ftt : Float
            Choix du type du filtre sur les grains.
        mul : float ou PyoObject
            Controle du volume de l'objet.

    '''
    def __init__(self, input, env, time=1, dens=100, filfrq=18000, ftt=2, mul=0.1):
        self.input = input
        #Longueur du son
        self.length = sndinfo(self.input)[1]
        #SampleRate du son
        self.sprate = sndinfo(self.input)[2]
        #SndTable
        self.soundtable = SndTable(self.input, start=0, stop=self.length)
        #Metro/Trig
        self.met = Metro(time=time).play()
        #Automatisation de la position
        self.random = TrigRand(self.met, min=1, max=self.sprate*self.length, port=0.05)
        #Particle2 pour la position
        self.parti = Particle2(self.soundtable, env, dens=dens, pitch=1, pos=self.random, filterfreq=filfrq, filtertype=ftt,
                                        mul=mul)

    def out(self, chnl=0):
        "Signal audio en sortie"
        self.parti.out(chnl)
        return self
        
    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.parti
        
#SECTION TEST#
if __name__ == "__main__":

    TEST = 2

    audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
    audioServer.start()    

    env = CosTable(list=[(0,0.0000), (2000, 0.7), (3970,0.8133), (5000, 0.7), (8192,0.0000)])
    sound = 'vertflute.wav'

    if TEST == 1:
        autr = AutoR(sound, env, time=0.125, dens=250, filfrq=2000, ftt=2, mul=0.3).out()
        
    elif TEST == 2:
        autr = AutoR(sound, env, time=1, dens=500, filfrq=15000, ftt=0, mul=0.1).out()
        
    audioServer.gui(locals())