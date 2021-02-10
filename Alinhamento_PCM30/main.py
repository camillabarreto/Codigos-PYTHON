#!/usr/bin/env python3

import sys

# PAQ = X0011011
PAQ1 = '10011011'
PAQ2 = '00011011'
LENGTH_FRAME = 256

# States
REALIGNING_BIT = 0
REALIGNING_FRAME = 1
ALIGNED = 2

# Global Variables
current_state = 0
b = -1
bf = 0
bit1 = False
paq_lost = 0

def FSM(byte):
    switch = {
        REALIGNING_BIT: realigning_bit,
        REALIGNING_FRAME: realigning_frame,
        ALIGNED: aligned
    }
    # Executa a função do estado atual
    func = switch.get(current_state, lambda: None)
    return func(byte)

def realigning_bit(byte):
    if byte == PAQ1 or byte == PAQ2:
        print('realigning_bit:   ', byte,'     bit ', b)
        global current_state
        current_state = REALIGNING_FRAME

def realigning_frame(byte):
    global current_state, b
    global bit1

    print('realigning_frame: ', byte, '     bit ', bf)
    
    if not bit1:
        if byte[1] == '1': bit1 = True
        else: current_state = REALIGNING_BIT

    elif byte == PAQ1 or byte == PAQ2:
        bit1 = False
        current_state = ALIGNED
    else:
        current_state = REALIGNING_BIT
        bit1 = False

def aligned(byte):
    print('aligned:          ', byte, '     bit ', bf)
    global paq_lost, current_state
    if byte != PAQ1 and byte != PAQ2:
        paq_lost += 1
        if paq_lost == 3:
            print('===== LOST =====')
            current_state = REALIGNING_BIT
            paq_lost = 0
    else: paq_lost = 0


if __name__ == '__main__':

	# File

    try:
        arq_r = open(sys.argv[1], 'r')
    except Exception as e:
        print('Não conseguiu acessar arquivo', e)
        sys.exit(0)
    
    try:
        arq_w = open("data_new", 'w')
    except Exception as e:
        print('Não conseguiu acessar arquivo', e)
        sys.exit(0)
    
    arq_w.flush()
    i = arq_r.readline()
    while i:
        i = i.replace(" ", "")
        i = i.replace("\n", "")
        arq_w.write(i)
        x = bytearray()
        i = arq_r.readline()

    arq_w.close()
    try:
        arq = open("data_new", 'r')
    except Exception as e:
        print('Não conseguiu acessar arquivo', e)
        sys.exit(0)
   
    # State Machine

    print('\n\nINICIANDO ALGORITMO\n\n')

    s = arq.readline()
    global b
    global bf
    result = False
    while (not result):
        if current_state == REALIGNING_BIT:
            b += 1
            byte = s[b : b + 8]
        elif current_state == REALIGNING_FRAME:
            if not bit1:
                bf = b + LENGTH_FRAME
                byte = s[bf : bf  + 8]
            else:
                bf +=LENGTH_FRAME
                byte = s[bf :bf + 8]
        elif current_state == ALIGNED:
            bf += 2 * LENGTH_FRAME
            b = bf
            byte = s[bf:bf + 8]

        if len(byte) < 8:
            break

        result = FSM(byte)
    
    print('\n\nFIM DO ARQUIVO\n\n')










 # Conversion : string to bytes

    # s = arq.readline()
    # base = 128
    # x = 0
    # raw = bytearray()
    # for i in range(0, len(s)):
    #     if s[i] == '1':
    #         x += base
    #     base = int(base / 2)
    #     if base == 0:
    #         raw.append(x)
    #         base = 128
    #         x = 0

    # Comparing with PAQ

    # sys.exit(0)
    # for i in range(0,len(s)-8):
    #     # print('BYTE: ', bin(i))
    #     x = s[i:i+8]
    #     # print(x)
    #     if x == PAQ1 or x == PAQ2:
    #         print('BYTE: ', x)
    #         print(i)
