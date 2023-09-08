#!/usr/bin/env python3
import socket
import sys
import threading

#--------------------------------------------------------------
# FUNÇÕES

def TrataSensor(conn):
    while True:
        data = conn.recv(1000)
        if not data:
            break
        else:
            print('recebi ', len(data), ' bytes')
            print(data)

    conn.close()    
    print('O cliente', conn, 'encerrou')

#--------------------------------------------------------------
# PROGRAMA PRINCIPAL

HOST = ''               # ANY_IP = todos os IPs do HOST
SENSORES={}     # lista de sensores conectados
CONSOLE=None  # conexao com o console remoto

print('Entre com a porta do servidor')
PORTA= int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORTA))
except:
   print('# erro de bind')
   sys.exit()

s.listen(5)

print('aguardando conexoes em ', PORTA)

#--------------------------------------------------------------
# LOOP para tratar clientes

while True:
    conn, addr = s.accept()
    print('recebi uma conexao de ', addr)
    TrataSensor(conn) 
    print('o cliente encerrou')
    conn.close()
#--------------------------------------------------------------

print('o servidor encerrou')
s.close()