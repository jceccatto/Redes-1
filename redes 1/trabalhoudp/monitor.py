# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:26:47 2019

@author: Jh
"""

#!/usr/bin/env python3
import socket
import sys
import threading
import time

SENSORES = {}
ACK = False

#---------------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
#---------------------------------------------------------------------------------

def recebeComando(s):
   
    global SENSORES
    global ACK
   
    while True:
        try:
            data, addr = s.recvfrom(1460)
            if(len(data) > 100):
                continue
            strdata = str(data,'utf-8')
        except:
            print('O sensor foi encerrado')
            continue

        try:
            (comando, dado) = strdata.split(' ',1)
        except:
            print('\r\nComando invalido do sensor', addr)
            continue
        if comando == 'REGISTRO':
            SENSORES[dado] = addr
            print('O sensor ' + dado + ' registrou')
            s.sendto(bytes('ACKregistro','utf-8'), addr)
            # ------------------------------------------------------------  EXERCICIO 1A
               
        elif comando == 'ESTADO':
            if addr not in SENSORES.values():
                ID = 'DESCONHECIDO'
            for ID,a in SENSORES.items():
                if a == addr:
                    break
            print('\r\nSensor ' + ID + ' enviou ' + dado + '\r\n')
           
        # --------------------------------------------------------------  EXERCICIO 2B
        elif comando == 'ACKcomando':
            if addr not in SENSORES.values():
                ID = 'DESCONHECIDO'
            for ID,a in SENSORES.items():
                if a == addr:
                    break
            if ID != 'DESCONHECIDO':
                ACK=True
                print('O sensor ', ID, ' confirmou o comando')
         
# --------------------------------------------------------------------- EXERCICIO 2C
def transmissaoConfiavel(s, addr, dados):
    global ACK
    try:
        s.sendto(bytes(dados, 'utf-8'), addr)
    except:
        print('O sensor foi encerrado')
    time.sleep(5)
    return ACK 
           
def enviaComando(s):
    global ACK
   
    dados = input()
    print('...\r\n')

    # Separa o SENSOR_ID do COMANDO
    try:
        (sensor, comando) = dados.split(' ',1)
    except:
        return

    # Envia o comando para o sensor apenas se ele estiver registrado
    if sensor in SENSORES:   
        # ---------------------------------------------------------------- EXERCICIO 2D
             
        #s.sendto(bytes(comando, 'utf-8'), SENSORES[sensor])  
        ACK=False
        for i in range(3):
            if transmissaoConfiavel(s, SENSORES[sensor], comando ):
                break
            else:
                print('Nova tentativa: ', i)
                
    else:
        print('\r\nEste sensor não existe')

#------------------------------------------------------------------------------------------
# PROGRAMA PRICIPAL
#------------------------------------------------------------------------------------------

print('\r\nEntre com a porta do servidor')
porta = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         
try:
    s.bind(('', porta))
except:
    print('# erro de bind')
    sys.exit()

t = threading.Thread( target=recebeComando, args=(s,))
t.start()

print('\r\nDigite SENSOR_ID COMANDO')
   
while True:
    enviaComando(s)
    time.sleep(1)

print('\r\no servidor encerrou')
s.close()