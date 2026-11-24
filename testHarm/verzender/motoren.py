# motoren.py
# Alle functies die de motoren aansturen.

from microbit import *

# pin defines
rechts_vooruit = pin12       # rechts vooruit
rechts_achteruit = pin8      # rechts achteruit
links_vooruit = pin16        # links vooruit
links_achteruit = pin0       # links achteruit

# in te vullen waardes:
# PWM-frequentie: hoe vaak per seconde de pin aan/uit schakelt
FREQUENTIE = 500        # in Hz

# Snelheden, duty-cycle in %
SNEL_PROCENT = 60       # normaal vooruit
BIJSTUREN_PROCENT = 30  # langzame kant bij bijsturen
DRAAIEN_PROCENT = 30    # snelheid bij draaien op de plek

# omrekeningen:
# omrekenen van duty-cycle in % naar PWM-waarde (0 t/m 1023)
SNEL = SNEL_PROCENT * 1023 // 100
BIJSTUREN = BIJSTUREN_PROCENT * 1023 // 100
DRAAIEN = DRAAIEN_PROCENT * 1023 // 100
# van frequentie naar periode in microseconden
periode = 1000000 // FREQUENTIE

# onthoudt wat de motoren nu doen, zodat communicatie.py dit kan doorsturen
actie = 'stoppen'

# stel voor alle vier de pinnen de PWM-periode in
for pin in [rechts_vooruit, rechts_achteruit, links_vooruit, links_achteruit]:
    pin.set_analog_period_microseconds(periode)


def motoren(rechts_v, links_v, rechts_a, links_a):
    rechts_vooruit.write_analog(rechts_v)
    links_vooruit.write_analog(links_v)
    rechts_achteruit.write_analog(rechts_a)
    links_achteruit.write_analog(links_a)


def vooruit():
    global actie
    actie = 'vooruit'
    motoren(SNEL, SNEL, 0, 0)

def links_bijsturen():
    global actie
    actie = 'links_bijsturen'
    # rechts sneller dan links, dus de wagen gaat naar links
    motoren(SNEL, BIJSTUREN, 0, 0)

def rechts_bijsturen():
    global actie
    actie = 'rechts_bijsturen'
    # links sneller dan rechts, dus de wagen gaat naar rechts
    motoren(BIJSTUREN, SNEL, 0, 0)

def stoppen():
    global actie
    actie = 'stoppen'
    motoren(0, 0, 0, 0)

def rechts_draaien():
    global actie
    actie = 'rechts_draaien'
    # links vooruit, rechts achteruit: draaien op de plek naar rechts
    motoren(0, DRAAIEN, DRAAIEN, 0)

def links_draaien():
    global actie
    actie = 'links_draaien'
    # rechts vooruit, links achteruit: draaien op de plek naar links
    motoren(DRAAIEN, 0, 0, DRAAIEN)
