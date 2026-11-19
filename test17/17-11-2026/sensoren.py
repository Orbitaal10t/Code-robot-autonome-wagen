from microbit import *
import time
import machine

def meet_lijnsensoren():
    links= pin2.read_digital()
    rechts=pin9.read_digital()
    print(links,rechts)
    return links,rechts


def afstand_vooruit():
    pin1.write_digital(0)
    time.sleep_us(2)
    pin1.write_digital(1)
    time.sleep_us(10)
    pin1.write_digital(0)
    tijd=machine.time_pulse_us(pin13,1,3000)
    afstandV=tijd/58
    return afstandV
    
def afstand_rechts():
    pin3.write_digital(0)
    time.sleep_us(2)
    pin3.write_digital(1)
    time.sleep_us(10)
    pin3.write_digital(0)
    tijd=machine.time_pulse_us(pin14,1,3000)
    afstandR=tijd/58
    return afstandR   

def afstand_links():
    pin4.write_digital(0)
    time.sleep_us(2)
    pin4.write_digital(1)
    time.sleep_us(10)
    pin4.write_digital(0)
    tijd=machine.time_pulse_us(pin15,1,3000)
    afstandL=tijd/58
    return afstandL   