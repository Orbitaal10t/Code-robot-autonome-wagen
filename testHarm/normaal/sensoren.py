# sensoren.py
# alle functies die iets met meten te maken hebben

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
    # de pinnen worden aangeroepen via de aanroep zelf

    # 1. korte triggerpuls van 10 microseconden geven
    trig.write_digital(0)
    time.sleep_us(2)
    trig.write_digital(1)
    time.sleep_us(10)
    trig.write_digital(0)

    # 2. meten hoe lang de echo-pin hoog (1) blijft, maximaal 3000 us wachten.
    tijd = machine.time_pulse_us(echo, 1, 3000)

    # 3. geen echo? dan negatief getal, buiten bereik dus hoog getal terug geven:
    if tijd < 0:
        return 999

    # 4. tijd omrekenen naar cm, komt uit datasheet
    return tijd / 58

# alleen juiste pins invullen
def afstand_vooruit():
    return meet_afstand(pin1, pin13)

def afstand_rechts():
    return meet_afstand(pin3, pin14)

def afstand_links():
    return meet_afstand(pin4, pin15)
