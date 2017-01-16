#Main Start

from pyo import *
s = Server().boot()

a = Sine().out()

s.gui(locals())

