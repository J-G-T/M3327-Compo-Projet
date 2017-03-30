from pyo import *


class PRead:
    '''
    Lecteur de son via objet Pointer2 et SndTable.
    
    Arguments:
        Input : PyoObject
            Input en entree de l'effet.
        spd : PyoObject ou Float        
            Vitesse de lecture de la table
        min : PyoObject ou Float 
            Point de depart de la lecture du son, de 0 a 1 ou 0 est le debut du 0 et 1 sa fin.
        max : PyoObject ou Float 
            Point final de la lecture du son.
        mul : float ou PyoObject
            Controle du volume de l'objet.

    '''
    def __init__(self, input, spd=0.7, min=0.66, max=0.8, mul=0.5):
        self.input = input
        #Longueur du son
        self.length = sndinfo(self.input)[1]
        #SndTable
        self.sndtable = SndTable(self.input, start=0, stop=self.length)
        #Initialisation du controle de l'index
        self.ind = Sine(spd).range(min, max)
        #Pointer pour lire la table selon l'index
        self.point = Pointer2(self.sndtable, self.ind, mul=mul)

    def out(self, chnl=0):
        "Signal audio en sortie"
        self.point.out(chnl)
        return self

    def sig(self):
        "Retourne le signal audio de la classe, pour le post-traitement."
        return self.point
        
#SECTION TEST#
if __name__ == "__main__":

    TEST = 2

    audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
    audioServer.start()    

    sound = 'mota.wav'

    if TEST == 1:
        pr = PRead(sound, spd=0.4, min=0.1, max=0.5, mul=0.3).out()
        
    elif TEST == 2:
        pr2 = PRead(sound, spd=7, min=0.4, max=0.42, mul=0.3).out()
        
    audioServer.gui(locals())