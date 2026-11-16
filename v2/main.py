from microbit import *
import sensoren
import motoren

zoek_einde = False
uitvoeren = False
draaien_rechts = False
draaien_links = False
display.off()


motoren.stoppen()

print('configured for flight')
while True:
    if button_a.was_pressed() and not uitvoeren:
        uitvoeren = True
        print('start')

    if button_b.was_pressed() and uitvoeren:
        uitvoeren = False
        motoren.stoppen()

    if uitvoeren:
        links, rechts = sensoren.meet_lijnsensoren()
        AV = sensoren.afstand_vooruit()
        geluid=sensoren.geluid_nivea()
        heuvel=sensoren.heuvel_detectie()
        if draaien_rechts:
            if links == 1 and AV >= 7:
                motoren.stoppen()
                zoek_einde = False
                draaien_rechts = False
            else:
                motoren.rechts_draaien()

        elif draaien_links:
            if rechts == 1 and AV >= 7:
                motoren.stoppen()
                zoek_einde = False
                draaien_links = False
            else:
                motoren.links_draaien()
                
        elif geluid>=120:
            motoren.stoppen()

        elif heuvel < 30:
            motoren.stoppen()
            
        elif AV <= 6:
            motoren.stoppen()

        elif zoek_einde:
            motoren.vooruit_langzaam()
            if links == 0 and rechts == 0:
                motoren.stoppen()
                AR = sensoren.afstand_rechts()
                if AR >= 5:
                    draaien_rechts = True
                    motoren.rechts_draaien()
                else:
                    AL = sensoren.afstand_links()
                    if AL >= 5:
                        draaien_links = True
                        motoren.links_draaien()

        elif links == 0 and rechts == 0:
            if heuvel>65:
                motoren.vooruit_langzaam()
            else:
                motoren.vooruit()

        elif links == 1 and rechts == 0:
            if heuvel>65:
                motoren.links_bijsturen_langzaam()
            else:
                motoren.links_bijsturen()

        elif links == 0 and rechts == 1:
            if heuvel>65:
                motoren.rechts_bijsturen_langzaam()
            else:
                motoren.rechts_bijsturen()

        elif links == 1 and rechts == 1:
            zoek_einde = True
            motoren.vooruit_langzaam()
