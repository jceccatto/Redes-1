# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:30:14 2019

@author: Jh
"""

#!/usr/bin/env python3
import socket
import sys
import time
from random import randint

ESTADO='OFF'
ID = 'sala'

#---------------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
#---------------------------------------------------------------------------------

def interpretaComando(comando, addr):
    global ESTADO
   
    strcomando = str(comando,'utf-8').lower()
    print('Recebi o comando', strcomando)
    s.sendto(bytes('ACKcomando ' +ID , 'utf-8'), addr)
    #------------------------------------------------------------- EXERCICIO 2A
         
    if strcomando == 'ligar':
        ESTADO = 'ON'
    elif strcomando == 'desligar':
        ESTADO = 'OFF'
    elif strcomando == 'consulta':
        s.sendto(bytes('ESTADO '+ ESTADO, 'utf-8'), addr)
    else:
        print('comando desconhecido: ', comando)

def defineMonitor():
   
    print('IP do monitor: <ENTER>=localhost')
    ip = input()
    if not ip:
        ip = '127.0.0.1'

    print('PORTA do monitor: <ENTER>=9999')
    data = input()
    if not data:
        porta=9999
    else:
        porta=int(data)

    print('ID do sensor: <ENTER>=sala')
    ID = input()
    if not ID:
        ID='sala'

    return(ip, porta, ID)

# -------------------------------------------------------------------- EXERCICIO 1B
def registraSensor(s,ip,porta):
    s.sendto(bytes('REGISTRO '+ ID, 'utf-8'), (ip, porta))
    s.setblocking(0)
    time.sleep(5)
    try:
        data, addr = s.recvfrom(1024)
        strdata = str(data,'utf-8')
        if strdata == 'ACKregistro':
            print('registrado no monitor ', addr)
            return True
        else:
            return False
    except:
        print('\no monitor está desligado')
        return False

#------------------------------------------------------------------------------------------
# PROGRAMA PRICIPAL
#------------------------------------------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

(ip, porta, ID) = defineMonitor()

# -------------------------------------------------------------------- EXERCICIO 1C

#s.sendto(bytes('REGISTRO '+ ID, 'utf-8'), (ip, porta))
while True:
    if registraSensor(s, ip, porta):
        break
s.setblocking(1)  

while True:
    data, addr = s.recvfrom(1024)
    if randint(1,2) is not 2:   # simula taxa de 50% de perdas
        interpretaComando(data, (ip,porta))

print('o monitor encerrou')
s.close()