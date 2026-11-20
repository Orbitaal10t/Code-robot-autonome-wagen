# motoren.py
# Alle functies die de motoren aansturen.

from microbit import *

# Welke pin hoort bij welke motorrichting
rechts_vooruit = pin12       # rechts vooruit
rechts_achteruit = pin8      # rechts achteruit
links_vooruit = pin16        # links vooruit
links_achteruit = pin0       # links achteruit

# PWM-frequentie: hoe vaak per seconde de pin aan/uit schakelt
frequentie = 500                    # Hz
periode = 1000000 // frequentie


# Snelheden, duty-cycle in %
SNEL = 60       # normaal vooruit
BIJSTUREN = 30  # langzame kant bij bijsturen
DRAAIEN = 30    # snelheid bij draaien op de plek

# omrekening van duty-cycle in percentage naar PWM-signaal
snel = 100 // 1023 *  SNEL
bijsturen = 100 // 1023 *  BIJSTUREN
draaien = 100 // 1023 *  DRAAIEN

# Stel voor alle vier de pinnen de PWM-periode in
for pin in [rechts_vooruit, rechts_achteruit, links_vooruit, links_achteruit]:
    pin.set_analog_period_microseconds(periode)


def motoren(rechts_v, links_v, rechts_a, links_a):
    # De basisfunctie: zet een snelheid op alle vier de pinnen.
    # Alle functies hieronder gebruiken deze.
    rechts_vooruit.write_analog(rechts_v)
    rechts_achteruit.write_analog(links_v)
    links_vooruit.write_analog(rechts_a)
    links_achteruit.write_analog(links_a)


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
