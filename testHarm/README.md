# testHarm

## verzender (micro:bit in de wagen)
Zet alle vier de bestanden op de micro:bit in de wagen:
- `main.py` - de toestanden en het rijden
- `sensoren.py` - lijnsensoren en ultrasoon sensoren
- `motoren.py` - motoren aansturen
- `communicatie.py` - stuurt 5x per seconde de metingen via de radio

## ontvanger (micro:bit aan de computer)
Zet alleen `ontvanger/main.py` op de tweede micro:bit en laat hem met USB aan de computer zitten.
Open daarna https://htools.nl/robot in Chrome of Edge en klik op "Verbinden".

Display van de ontvanger: knipperende stip = berichten van de wagen, kruis = niets ontvangen.

## Pinnen
| Onderdeel | Pin(nen) |
|---|---|
| Lijnsensor links / rechts | pin2 / pin9 |
| Ultrasoon vooruit | trig pin1, echo pin13 |
| Ultrasoon rechts | trig pin3, echo pin14 |
| Ultrasoon links | trig pin4, echo pin15 |
| Motor rechts vooruit / achteruit | pin12 / pin8 |
| Motor links vooruit / achteruit | pin16 / pin0 |

## Radiobericht
Groep 42, kanaal 7 (in `communicatie.py` en `ontvanger/main.py` gelijk houden).

`AW,teller,rijdt,draaien,actie,lijn_links,lijn_rechts,vooruit,rechts,links`

Voorbeeld: `AW,57,1,-,vooruit,0,0,23,-,-`
- afstanden in hele cm, `999` = buiten bereik (verder dan ca. 51 cm), `-` = niet gemeten
- de ontvanger zet de signaalsterkte (dBm) er achteraan

`test_harm.hex` is de oude versie zonder radio.
