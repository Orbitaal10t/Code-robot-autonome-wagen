# main.py

# er zijn 4 toestanden die de wagen aan kan nemen, in volgorde van prioriteit:
#    1. draaien            draaien naar links of rechts en draait tot de lijn weer gevonden is.
#    2. stoppen            stopt voor obstakel, voor slagboom én veiligheid.
#    3. kruising           beide lijnsensoren zien een lijn en er wordt rechtdoor, rechts of links gekozen.
#    4. lijnen volgen      dus recht door rijden.
# de eerste toestand die waar is wordt uitgevoerd, de rest wordt die ronde overgeslagen.
# aan het eind van elke ronde stuurt communicatie.py (5x per seconde) de metingen naar de computer.

from microbit import *
import sensoren
import motoren
import communicatie

#defines
uitvoeren = False       # rijdt de wagen? (knop A of website = start, knop B of website = stop)
draaien = None          # None = niet draaien, anders 'rechts_draaien' of 'links_draaien'
draai_start = 0         # moment waar het draaien begint om op verder te tellen
afstand_rechts = None   # None = nog niet gemeten sinds het laatste radiobericht
afstand_links = None

# in tevullen waardes:
MIN_DRAAITIJD = 800     # minimale tijd in ms dat de robot moet draaien
DRAAI_AFSTAND = 15      # in cm, wanneer de weg vrij is om daar heen te draaien
MOMENT_WEGHALEN = 500   # het aantal ms dat de wagen stopt om het moment uit de wagen te halen
ACHTERUIT_AFSTAND = 9   # in cm, wat ver de voorste sensor moet zien om te stoppen met achteruit rijden

display.off()       # display uit, zodat pinnen 3, 4 en 9 vrij zijn voor de sensoren
motoren.stoppen()
print('configured for flight')

while True:
    # starten en stoppen kan met de knoppen of op afstand via de website
    opdracht = communicatie.ontvang_opdracht()     # 'START', 'STOP' of None

    if (button_a.was_pressed() or opdracht == 'START') and not uitvoeren:
        uitvoeren = True
        print('start')

    if (button_b.was_pressed() or opdracht == 'STOP') and uitvoeren:
        uitvoeren = False
        draaien = None
        motoren.stoppen()

    if not uitvoeren:
        # wagen staat stil: alle sensoren meten en versturen,
        # zo kun je met je hand testen of alles werkt
        if communicatie.tijd_voor_bericht():
            lijn_links, lijn_rechts = sensoren.meet_lijnsensoren()
            vooruit = sensoren.afstand_vooruit()
            sleep(20)   # even wachten zodat de echo van de vorige sensor weg is
            rechts = sensoren.afstand_rechts()
            sleep(20)
            links = sensoren.afstand_links()
            communicatie.verstuur(uitvoeren, draaien, motoren.actie,
                                  lijn_links, lijn_rechts, vooruit, rechts, links)
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
        if lang_genoeg and lijn_rechts == 0 and lijn_links == 1 and afstand_vooruit >= 25:
            motoren.stoppen()
            draaien = None
            sleep(MOMENT_WEGHALEN)  # het volledige moment er uit halen
        else:
            motoren.rechts_draaien()

    elif draaien == 'links_draaien':
        lang_genoeg = running_time() - draai_start >= MIN_DRAAITIJD  # True wanneer lang genoeg gedraaid
        # zo wordt de evt lijn waar hij op zit genegeerd
        # daarna draaien tot de lijn weer goed onder de wagen ligt
        if lang_genoeg and lijn_links == 0 and lijn_rechts == 1 and afstand_vooruit >= 25:
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
        afstand_rechts = sensoren.afstand_rechts()      # onthouden voor de radio
        # achteruit rijden begint hier
        if afstand_rechts >= DRAAI_AFSTAND:
            motoren.stoppen()
            sleep(MOMENT_WEGHALEN)
            motoren.achteruit()
            while sensor.afstand_vooruit <= ACHTERUIT_AFSTAND: # nu ingesteld op 9cm   
                sleep(MOMENT_WEGHALEN)    # achteruit rijden stopt hier
            else:
                motoren.achteruit()       # achteruit rijden blijft gaan tot de afstand behaald is.
            draaien = 'rechts_draaien'
            draai_start = running_time()    # onthoud wanneer het draaien begon
            motoren.rechts_draaien()

        else:
            afstand_links = sensoren.afstand_links()    # afstand_links alleen meten als rechts dicht is
            if afstand_links >= DRAAI_AFSTAND:
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

    # metingen doorsturen naar de computer (communicatie.py bepaalt of het al tijd is)
    if communicatie.tijd_voor_bericht():
        communicatie.verstuur(uitvoeren, draaien, motoren.actie, lijn_links, lijn_rechts,
                              afstand_vooruit, afstand_rechts, afstand_links)
        # links en rechts zijn verstuurd, weer leeg maken tot de volgende kruising
        afstand_rechts = None
        afstand_links = None
