from microbit import *

rv= pin12
ra= pin8
lv=pin16
la=pin0


freqeuntie=500
periode=1000000//freqeuntie

v=600
B=300
l=400

motor_pinnen=[rv,ra,lv,la]
for pin in motor_pinnen:
    pin.set_analog_period_microseconds(periode) 
    
def motoren(rechtsV,linksV,rechtsA,linksA):
    rv.write_analog(rechtsV)
    lv.write_analog(linksV)
    la.write_analog(linksA)
    ra.write_analog(rechtsA)
    
def vooruit():
    motoren(v,v,0,0)

def rechts_bijsturen():
    motoren(B,v,0,0)
    
def links_bijsturen():
    motoren(v,B,0,0)
    
def stoppen():
    motoren(0,0,0,0)

def rechts_draaien():
    motoren(0,300,300,0)

def links_draaien():
    motoren(300,0,0,300)

def vooruit_langzaam():
    motoren(l,l,0,0)
