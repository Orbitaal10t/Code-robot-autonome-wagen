from microbit import *

def meet_lijnsensoren():
    links= pin2.read_digital()
    rechts=pin9.read_digital()
    print(links,rechts)
    return links,rechts


