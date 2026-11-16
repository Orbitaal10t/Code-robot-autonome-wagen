from microbit import *

rv= pin12
ra= pin8
lv=pin16
la=pin0

freqeuntie=6000
periode=1000000//freqeuntie
vooruitrijden=800
langzaamvooruit=400
bijsturen=400
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
    motoren(vooruitrijden,vooruitrijden,0,0)

def rechts_bijsturen():
    motoren(bijsturen,vooruitrijden,0,0)
    
def links_bijsturen():
    motoren(vooruitrijden,bijsturen,0,0)
    
def stoppen():
    motoren(0,0,0,0)

def rechts_draaien():
    motoren(0,vooruitrijden,0,0)

def links_draaien():
    motoren(vooruitrijden,0,0,0)

def vooruit_langzaam():
    motoren(langzaamvooruit,langzaamvooruit,0,0)
    
def rechts_bijsturen_langzaam():
    motoren(300, langzaamvooruit, 0, 0)


def links_bijsturen_langzaam():
    motoren(langzaamvooruit, 300, 0, 0)
