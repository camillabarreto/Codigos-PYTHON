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

# Colors
RED = '\033[41m'
YELLOW = '\033[43m'
GREEN = '\033[42m'
BLUE = '\033[44m'
RST = '\033[0;0m'

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
    func = switch[current_state]
    return func(byte)

def realigning_bit(byte):
    if byte == PAQ1 or byte == PAQ2:
        print(BLUE+'STATE realigning_bit:   ', byte,'     bit ', b, RST)
        global current_state
        current_state = REALIGNING_FRAME

def realigning_frame(byte):
    global current_state
    global bit1
    
    if not bit1:
        if byte[1] == '1': bit1 = True
        else: current_state = REALIGNING_BIT

    elif byte == PAQ1 or byte == PAQ2:
        bit1 = False
        current_state = ALIGNED
        print(GREEN+'STATE realigning_frame: ', byte, '     bit ', bf, RST)
        print("FRAME(",b,"): ", s[b:b+LENGTH_FRAME])
        print("FRAME(",b+LENGTH_FRAME,"):", s[b+LENGTH_FRAME:b+(2*LENGTH_FRAME)])
        return
        
    else:
        current_state = REALIGNING_BIT
        bit1 = False
    
    print('STATE realigning_frame: ', byte, '     bit ', bf)

def aligned(byte):
    global paq_lost, current_state
    if byte != PAQ1 and byte != PAQ2:
        paq_lost += 1
        if paq_lost == 3:
            print(RED+'STATE aligned:          ', byte, '     bit ', bf, RST)
            current_state = REALIGNING_BIT
            paq_lost = 0
        else:
            print(YELLOW+'STATE aligned:          ', byte, '     bit ', bf, RST)
            print("FRAME(",b,"):", s[b:b+LENGTH_FRAME])
            print("FRAME(",b+LENGTH_FRAME,"): ", s[b+LENGTH_FRAME:b+(2*LENGTH_FRAME)])
    else:
        print(GREEN+'STATE aligned:          ', byte, '     bit ', bf, RST)
        print("FRAME(",b,"):", s[b:b+LENGTH_FRAME])
        print("FRAME(",b+LENGTH_FRAME,"):", s[b+LENGTH_FRAME:b+(2*LENGTH_FRAME)])
        paq_lost = 0



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
   

    # Instructions

    print('\n\nSINALIZAÇÃO DE CORES\n\n')
    print('+ '+BLUE,'AZUL    ',RST+" : possível início de quadro")
    print('+ '+GREEN,'VERDE   ',RST+" : confirmado início de quadro")
    print('+ '+RED,'VERMELHO',RST+" : perdeu alinhamento")

    # State Machine

    print('\n\nINICIANDO ALGORITMO\n\n')

    s = arq.readline()
    b = 0
    bf = -1
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
            b = bf
            bf += 2 * LENGTH_FRAME
            byte = s[bf:bf + 8]

        if len(byte) < 8:
            break

        result = FSM(byte)
    
    print('\n\nFIM DO ARQUIVO\n\n')