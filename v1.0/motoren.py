from microbit import *

rv= pin12
ra= pin8
lv=pin16
la=pin0

freqeuntie=6000
periode=1000000//freqeuntie

motor_pinnen=[rv,ra,lv,la]
for pin in motor_pinnen:
    pin.set_analog_period_microseconds(periode) 
    
def motoren(rechtsV,linksV,rechtsA,linksA):
    global laatste_waarden
    rv.write_analog(rechtsV)
    lv.write_analog(linksV)
    la.write_analog(linksA)
    ra.write_analog(rechtsA)
    
def vooruit():
    motoren(800,800,0,0)

def rechts_bijsturen():
    motoren(200,800,0,0)
    
def links_bijsturen():
    motoren(800,200,0,0)
    
def stoppen():
    motoren(0,0,0,0)

