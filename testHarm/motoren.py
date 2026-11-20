# motoren.py
# Alle functies die de motoren aansturen.

from microbit import *

# Welke pin hoort bij welke motorrichting
rv = pin12   # rechts vooruit
ra = pin8    # rechts achteruit
lv = pin16   # links vooruit
la = pin0    # links achteruit

# PWM-frequentie: hoe vaak per seconde de pin aan/uit schakelt
frequentie = 500                    # Hz
periode = 1000000 // frequentie     # in microseconden (// = delen zonder komma)

# Snelheden. PWM-waarde van 0 (uit) tot 1023 (vol)
SNEL = 600       # normaal vooruit
BIJSTUREN = 300  # langzame kant bij bijsturen
DRAAIEN = 300    # snelheid bij draaien op de plek

# Stel voor alle vier de pinnen de PWM-periode in
for pin in [rv, ra, lv, la]:
    pin.set_analog_period_microseconds(periode)


def motoren(rechts_v, links_v, rechts_a, links_a):
    # De basisfunctie: zet een snelheid op alle vier de pinnen.
    # Alle functies hieronder gebruiken deze.
    rv.write_analog(rechts_v)
    lv.write_analog(links_v)
    ra.write_analog(rechts_a)
    la.write_analog(links_a)


def vooruit():
    motoren(SNEL, SNEL, 0, 0)

def links_bijsturen():
    # rechts sneller dan links, dus de wagen gaat naar links
    motoren(SNEL, BIJSTUREN, 0, 0)

def rechts_bijsturen():
    # links sneller dan rechts, dus de wagen gaat naar rechts
    motoren(BIJSTUREN, SNEL, 0, 0)

def stoppen():
    motoren(0, 0, 0, 0)

def rechts_draaien():
    # links vooruit, rechts achteruit: draaien op de plek naar rechts
    motoren(0, DRAAIEN, DRAAIEN, 0)

def links_draaien():
    # rechts vooruit, links achteruit: draaien op de plek naar links
    motoren(DRAAIEN, 0, 0, DRAAIEN)
