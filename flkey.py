#!/usr/bin/env python3

import mido
import random
from time import sleep

print(mido.get_output_names())


"""
F0 00 20 29 02 10 01 50 75 00 50 73 00 - header
50 6A 00 50 6B 00 43 - more header?
70 - position
4A 07 06 40 - unknown
71 - position
03 - color
F7 - end
"""

def create_pkt(color, pos):
    if (pos >= 16 or pos < 0):
        return(0)
    color = color.to_bytes(3, "big").hex().upper()
    j = 0

    msghex ='F0 00 20 29 02 10 01 50 75 00 50 73 00 50 6A 00 50 6B 00 43 '

    if (pos < 8):
        msghex += (((pos + 0x60).to_bytes(1, "big")).hex()).upper()
    else:
        msghex += (((pos + 0x68).to_bytes(1, "big")).hex()).upper()

    for i in color:
        j += 1
        if (j % 2):
            msghex += ' ' + color[j - 1:j + 1]

    msghex += ' F7'
    return mido.Message.from_hex(msghex)

def set_color(color, pos):
    with mido.open_output('FLkey Mini DAW In') as outport:
        outport.send(create_pkt(color, pos))

def refresh():
    refresh = mido.Message.from_hex('F0 00 20 29 02 10 01 50 75 00 50 73 00 F7')
    with mido.open_output('FLkey Mini DAW In') as outport:
        outport.send(refresh)



for i in range(0, 10):
    for i in range(0, 16):
        set_color(random.randint(0,127) << 16 | random.randint(0,127) << 8 | random.randint(0,127),i)
    sleep(0.3)
refresh()


