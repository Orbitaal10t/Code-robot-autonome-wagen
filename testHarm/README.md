# testHarm

Er zijn twee versies:
- `zonder_communicatie/` - de wagen zonder radio. **Hierin passen we de code aan.**
- `met_communicatie/` - dezelfde wagen met radio naar de computer (htools.nl/robot). Wordt pas bijgewerkt als we met radio gaan testen.

`motoren.py` en `sensoren.py` zijn in beide versies gelijk; alleen `main.py` verschilt (plus `communicatie.py` en de ontvanger).

Elke map heeft een `.hex`: sleep die naar de micro:bit (of open hem in python.microbit.org), dan staan alle bestanden er in een keer op.

## zonder_communicatie (micro:bit in de wagen)
`wagen_zonder_radio.hex`, of zet `main.py`, `sensoren.py` en `motoren.py` op de micro:bit.
Knop A = start, knop B = stop.

# met_communicatie

## verzender (micro:bit in de wagen)
`verzender/wagen_met_radio.hex`, of zet alle vier de bestanden op de micro:bit in de wagen:
- `main.py` - de toestanden en het rijden
- `sensoren.py` - lijnsensoren en ultrasoon sensoren
- `motoren.py` - motoren aansturen
- `communicatie.py` - stuurt 5x per seconde de metingen via de radio

## ontvanger (micro:bit aan de computer)
Zet `ontvanger/ontvanger.hex` (of alleen `ontvanger/main.py`) op de tweede micro:bit en laat hem met USB aan de computer zitten.
Open daarna https://htools.nl/robot in Chrome of Edge en klik op "Verbinden".

Met Start en Stop op de website (spatiebalk = stop) start en stop je de wagen op afstand; de ontvanger stuurt dan `CMD,START` of `CMD,STOP` via de radio. Knop A en B blijven werken.

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

