from microbit import *
import sensoren

import motoren


uitvoeren=False
display.off()

laatste_logtijd = running_time()
motoren.stoppen()

print('configured for flight')
while True:
    if button_a.was_pressed()and not uitvoeren:
        uitvoeren= True
        print('start')
        
    if button_b.was_pressed()and uitvoeren:
        uitvoeren= False
        motoren.stoppen()
        
    if uitvoeren:
        links,rechts=sensoren.meet_lijnsensoren()
        if links==0 and rechts==0:
            motoren.vooruit()
            
        elif links==1 and rechts==0:
            motoren.links_bijsturen()
            
        elif links==0 and rechts==1:
            motoren.rechts_bijsturen()
            
        elif links==1 and rechts==1:
            motoren.stoppen()
        
        
        

