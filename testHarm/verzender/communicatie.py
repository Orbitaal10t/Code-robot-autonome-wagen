# communicatie.py
# alles wat met de radio te maken heeft.
# de wagen stuurt 5x per seconde wat de sensoren zien naar de micro:bit aan de computer,
# en luistert of de computer START of STOP stuurt.

from microbit import running_time
import radio

# in te vullen waardes (moeten gelijk zijn aan die in de ontvanger!):
RADIO_GROEP = 42        # 0 t/m 255, eigen nummer zodat andere groepen ons niet storen
RADIO_KANAAL = 7        # 0 t/m 83
INTERVAL = 200          # ms tussen twee berichten, 200 ms = 5x per seconde

# radio aanzetten
# length = maximale berichtlengte in bytes, 64 is ruim genoeg voor ons bericht
# power = zendvermogen 0 t/m 7
radio.config(group=RADIO_GROEP, channel=RADIO_KANAAL, length=64, power=6)
radio.on()

laatste_bericht = 0     # moment (ms) waarop het laatste bericht verstuurd is
teller = 0              # telt de berichten, zo ziet de website of er berichten kwijt raken


def tijd_voor_bericht():
    # True als er sinds het laatste bericht INTERVAL ms voorbij is
    return running_time() - laatste_bericht >= INTERVAL


def afstand_tekst(afstand):
    # None = deze keer niet gemeten, dan sturen we een streepje
    if afstand is None:
        return '-'
    return str(int(afstand))    # hele cm is nauwkeurig genoeg


def verstuur(uitvoeren, draaien, actie, lijn_links, lijn_rechts, vooruit, rechts, links):
    # maakt één regel tekst van alle waardes en verstuurt die via de radio.
    # opbouw, gescheiden door komma's:
    #   AW, teller, rijdt (1/0), draaien (R/L/-), actie, lijn links, lijn rechts,
    #   afstand vooruit, afstand rechts, afstand links
    # voorbeeld: AW,57,1,-,vooruit,0,0,23,-,-
    global laatste_bericht, teller

    if draaien == 'rechts_draaien':
        draai = 'R'
    elif draaien == 'links_draaien':
        draai = 'L'
    else:
        draai = '-'

    bericht = ','.join([
        'AW',                           # AW = autonome wagen, herkenning voor de ontvanger
        str(teller),
        '1' if uitvoeren else '0',
        draai,
        actie,
        str(lijn_links),
        str(lijn_rechts),
        afstand_tekst(vooruit),
        afstand_tekst(rechts),
        afstand_tekst(links),
    ])
    radio.send(bericht)

    laatste_bericht = running_time()
    teller = (teller + 1) % 1000        # na 999 weer bij 0 beginnen


def ontvang_opdracht():
    # kijkt of er een opdracht van de computer binnen is.
    # geeft 'START', 'STOP' of None (niets ontvangen) terug.
    try:
        bericht = radio.receive()       # None als er niets is
    except ValueError:
        return None                     # kapot bericht, negeren
    if bericht and bericht.startswith('CMD,'):
        opdracht = bericht[4:]          # alles na 'CMD,'
        if opdracht in ('START', 'STOP'):
            return opdracht
    return None
