# main.py

# er zijn 4 toestanden die de wagen aan kan nemen, in volgorde van prioriteit:
#    1. draaien            draaien naar links of rechts en draait tot de lijn weer gevonden is.
#    2. stoppen            stopt voor obstakel, voor slagboom én veiligheid.
#    3. kruising           beide lijnsensoren zien een lijn en er wordt rechtdoor, rechts of links gekozen.
#    4. lijnen volgen      dus recht door rijden.
# de eerste toestand die waar is wordt uitgevoerd, de rest wordt die ronde overgeslagen.

from microbit import *
import sensoren
import motoren

#defines
uitvoeren = False       # rijdt de wagen? (knop A = start, knop B = stop)
draaien = None          # None = niet draaien, anders 'rechts_draaien' of 'links_draaien'
draai_start = 0         # moment waar het draaien begint om op verder te tellen

# in tevullen waardes:
MIN_DRAAITIJD = 300     # minimale tijd in ms dat de robot moet draaien
DRAAI_AFSTAND = 10      # afstand in cm
MOMENT_WEGHALEN = 500   # het aantal ms dat de wagen stopt om het moment uit de wagen te halen

display.off()       # display uit, zodat pinnen 3, 4 en 9 vrij zijn voor de sensoren
motoren.stoppen()
print('configured for flight')

while True:
    if button_a.was_pressed() and not uitvoeren:
        uitvoeren = True
        print('start')

    if button_b.was_pressed() and uitvoeren:
        uitvoeren = False
        draaien = None
        motoren.stoppen()

    if not uitvoeren:
        continue        # ga verder met de volgende "while True" ronde

    # uit lezen van sensoren:
    lijn_links, lijn_rechts = sensoren.meet_lijnsensoren()
    afstand_vooruit = sensoren.afstand_vooruit()

    # toestand 1: draaien, naar links of rechts en draait tot de lijn weer gevonden is
    # staat bovenaan: een bocht wordt altijd afgemaakt
    if draaien == 'rechts_draaien':
        lang_genoeg = running_time() - draai_start >= MIN_DRAAITIJD  # True wanneer lang genoeg gedraaid
        # zo wordt de evt lijn waar hij op zit genegeerd
        # daarna draaien tot de lijn weer goed onder de wagen ligt
        if lang_genoeg and lijn_rechts == 1 and lijn_links == 0 and afstand_vooruit >= 15:
            motoren.stoppen()
            draaien = None
            sleep(MOMENT_WEGHALEN)  # het volledige moment er uit halen
        else:
            motoren.rechts_draaien()

    elif draaien == 'links_draaien':
        lang_genoeg = running_time() - draai_start >= MIN_DRAAITIJD  # True wanneer lang genoeg gedraaid
        # zo wordt de evt lijn waar hij op zit genegeerd
        # daarna draaien tot de lijn weer goed onder de wagen ligt
        if lang_genoeg and lijn_links == 1 and lijn_rechts == 0 and afstand_vooruit >= 15:
            motoren.stoppen()
            draaien = None
            sleep(MOMENT_WEGHALEN)
        else:
            motoren.links_draaien()

    # toestand 2: stoppen, stopt voor obstakel, voor slagboom én veiligheid
    elif afstand_vooruit <= 4:
        motoren.stoppen()

    # toestand 3: kruising, beide lijnsensoren zien een lijn en er wordt iets gekozen
    elif lijn_links == 1 and lijn_rechts == 1:
        if sensoren.afstand_rechts() >= DRAAI_AFSTAND:
            motoren.stoppen()
            sleep(MOMENT_WEGHALEN)
            draaien = 'rechts_draaien'
            draai_start = running_time()    # onthoud wanneer het draaien begon
            motoren.rechts_draaien()
        elif sensoren.afstand_links() >= DRAAI_AFSTAND:   # afstand_links alleen meten als rechts dicht is
            motoren.stoppen()
            sleep(MOMENT_WEGHALEN)
            draaien = 'links_draaien'
            draai_start = running_time()    # onthoud wanneer het draaien begon
            motoren.links_draaien()
        else:
            motoren.vooruit()

    # toestand 4: lijn volgen, recht door rijden en lijn volgen
    elif lijn_links == 0 and lijn_rechts == 0:
        motoren.vooruit()

    elif lijn_links == 1 and lijn_rechts == 0:
        motoren.links_bijsturen()

    elif lijn_links == 0 and lijn_rechts == 1:
        motoren.rechts_bijsturen()
