# sensoren.py
# Alle functies die iets meten. main.py roept deze aan.

from microbit import *
import time
import machine

# owrd gevraagd door main
def meet_lijnsensoren():
    # lijnsensoren uitmeten, 1 is lijn 0 is geen lijn
    lijn_links = pin2.read_digital()
    lijn_rechts = pin9.read_digital()
    return lijn_links, lijn_rechts       
    # geeft twee waarden tegelijk terug


def meet_afstand(trig, echo):
    # Meet de afstand met een ultrasoonsensor (HC-SR04).
    #   trig = de pin waarop we de sensor laten "piepen"
    #   echo = de pin waarop de sensor het antwoord teruggeeft
    # Welke pinnen dat zijn, bepaalt degene die deze functie aanroept.

    # 1. Korte triggerpuls van 10 microseconden geven
    trig.write_digital(0)
    time.sleep_us(2)
    trig.write_digital(1)
    time.sleep_us(10)
    trig.write_digital(0)

    # 2. Meten hoe lang de echo-pin hoog (1) blijft, maximaal 3000 us wachten.
    #    3000 us komt overeen met ongeveer 51 cm.
    tijd = machine.time_pulse_us(echo, 1, 3000)

    # 3. Geen echo binnen de tijd? Dan geeft time_pulse_us een negatief getal (-1 of -2).
    #    Dat betekent: niets binnen bereik, dus vrij. We geven dan een groot getal terug.
    if tijd < 0:
        return 999

    # 4. Tijd omrekenen naar centimeters (geluid heen en terug: delen door 58)
    return tijd / 58


# Korte functies die alleen de juiste pinnen invullen.
# Zo staat in main.py een duidelijke naam in plaats van pinnummers.
def afstand_vooruit():
    return meet_afstand(pin1, pin13)

def afstand_rechts():
    return meet_afstand(pin3, pin14)

def afstand_links():
    return meet_afstand(pin4, pin15)
