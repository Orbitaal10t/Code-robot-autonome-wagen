# main.py (ontvanger)
# deze micro:bit zit met USB aan de computer.
# 1. hij vangt de radioberichten van de wagen op en stuurt ze via USB door
#    naar de website htools.nl/robot.
# 2. stuurt de website START of STOP, dan zendt hij dat via de radio naar de wagen.
# op het display: knipperende stip = er komen berichten binnen, kruis = niets van de wagen.

from microbit import *
import radio

# in te vullen waardes (moeten gelijk zijn aan die in communicatie.py van de wagen!):
RADIO_GROEP = 42
RADIO_KANAAL = 7

radio.config(group=RADIO_GROEP, channel=RADIO_KANAAL, length=64, power=7)
radio.on()

laatste_bericht = 0     # moment van het laatst ontvangen bericht
laatste_levensteken = 0 # moment van het laatste "ik leef nog" bericht naar de website
stip_aan = False
usb_tekst = ''          # wat er van de website binnenkomt, tot er een hele regel is

display.show(Image.NO)
print('ONTV,start')

while True:
    # ---- 1. radio van de wagen -> USB naar de website ----
    # receive_full geeft (bericht, signaalsterkte, tijd) of None als er niets is
    pakket = radio.receive_full()

    if pakket:
        bericht, sterkte, tijd = pakket
        # de eerste 3 bytes zijn een kopje van de radio zelf, de tekst begint daarna
        try:
            tekst = str(bericht[3:], 'utf8')
        except:
            tekst = ''      # kapot bericht, overslaan

        if tekst.startswith('AW,'):
            # signaalsterkte (dBm, bijv. -60) achteraan toevoegen en naar de computer sturen
            print(tekst + ',' + str(sterkte))
            laatste_bericht = running_time()

            # stip in het midden laten knipperen bij elk bericht
            stip_aan = not stip_aan
            display.clear()
            display.set_pixel(2, 2, 9 if stip_aan else 3)

    # ---- 2. USB van de website -> radio naar de wagen ----
    if uart.any():
        data = uart.read()
        if data:
            try:
                usb_tekst += str(data, 'utf8')
            except:
                usb_tekst = ''
            # zolang er een hele regel (met Enter) is: die afhandelen
            while '\n' in usb_tekst:
                regel, usb_tekst = usb_tekst.split('\n', 1)
                regel = regel.strip()
                if regel == 'START' or regel == 'STOP':
                    radio.send('CMD,' + regel)
                    print('ONTV,verstuurd,' + regel)
            if len(usb_tekst) > 50:
                usb_tekst = ''      # rommel zonder Enter, weggooien

    nu = running_time()

    # al 1 seconde niets gehoord van de wagen? kruis laten zien
    if laatste_bericht and nu - laatste_bericht > 1000:
        display.show(Image.NO)
        laatste_bericht = 0

    # elke 2 seconden een levensteken, zo weet de website dat de ontvanger werkt
    # (ook als de wagen uit staat)
    if nu - laatste_levensteken > 2000:
        print('ONTV,ok')
        laatste_levensteken = nu

    sleep(5)
