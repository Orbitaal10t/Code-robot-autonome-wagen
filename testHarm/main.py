# main.py
# Het hoofdprogramma. Gebaseerd op test17/17-11-2026, opgeschoond.
#
# De wagen kent drie toestanden:
#   1. lijn volgen      (draaien is None)
#   2. kruising         (beide lijnsensoren zien de lijn): kies een richting
#   3. draaien          (draaien is 'rechts' of 'links'): draai tot de lijn weer gevonden is

from microbit import *
import sensoren
import motoren

uitvoeren = False   # rijdt de wagen? (knop A = start, knop B = stop)
draaien = None      # None = niet draaien, anders 'rechts' of 'links'

display.off()       # display uit, zodat pinnen 3, 4 en 9 vrij zijn voor de sensoren
motoren.stoppen()
print('configured for flight')

while True:
    # ---------- Knoppen ----------
    if button_a.was_pressed() and not uitvoeren:
        uitvoeren = True
        print('start')

    if button_b.was_pressed() and uitvoeren:
        uitvoeren = False
        draaien = None
        motoren.stoppen()

    if not uitvoeren:
        continue    # niet rijden: sla de rest over en begin de lus opnieuw

    # ---------- Meten ----------
    links, rechts = sensoren.meet_lijnsensoren()
    AV = sensoren.afstand_vooruit()

    # ---------- Toestand 3: draaien ----------
    if draaien is not None:
        # Welke sensor moet de lijn weer zien? Bij rechtsom draaien de linker, en andersom.
        if draaien == 'rechts':
            buiten_sensor = links
        else:
            buiten_sensor = rechts

        if buiten_sensor == 1 and AV >= 15:
            # Lijn gevonden en vooruit is vrij: klaar met draaien
            motoren.stoppen()
            draaien = None
            sleep(100)
        elif draaien == 'rechts':
            motoren.rechts_draaien()
        else:
            motoren.links_draaien()

    # ---------- Obstakel vlak voor de wagen ----------
    elif AV <= 4:
        motoren.stoppen()

    # ---------- Toestand 1: lijn volgen ----------
    elif links == 0 and rechts == 0:
        motoren.vooruit()

    elif links == 1 and rechts == 0:
        motoren.links_bijsturen()

    elif links == 0 and rechts == 1:
        motoren.rechts_bijsturen()

    # ---------- Toestand 2: kruising (links == 1 en rechts == 1) ----------
    else:
        motoren.stoppen()
        sleep(100)

        if sensoren.afstand_rechts() >= 10:
            draaien = 'rechts'
            motoren.rechts_draaien()
        elif sensoren.afstand_links() >= 10:   # links alleen meten als rechts dicht is
            draaien = 'links'
            motoren.links_draaien()
        else:
            motoren.vooruit()
