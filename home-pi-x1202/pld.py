#!/usr/bin/env python3
#This python script is only suitable for UPS Shield X1200, X1201 and X1202

import gpiod
import time
from subprocess import call

PLD_PIN = 6
chip = gpiod.Chip('gpiochip4')
pld_line = chip.get_line(PLD_PIN)
pld_line.request(consumer="PLD", type=gpiod.LINE_REQ_DIR_IN)
try:
   while True:
       pld_state = pld_line.get_value()
       if pld_state == 1:
            time.sleep(1)
       else:
            time.sleep(1)
            call("sudo systemctl poweroff", shell=True)

finally:

   pld_line.release()