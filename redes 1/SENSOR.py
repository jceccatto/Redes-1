#!/usr/bin/env python3
import socket
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Entre com o IP do servidor')
IP= input()

print('Entre com a porta do servidor')
PORTA= int(input())

print('Entre com o ID do sensor')
ID= input()

try:
    s.connect((IP, PORTA))
except:
    print('erro de conexao')

# Envia o ID automaticamente após a conexão
s.send(bytes(ID, 'utf-8'))

# O sensor responde a mensagens de consulta enviando a hora local
while True: 
    data = s.recv(8)
    print(len(data),':', data)
    if data == b'CONSULTA':
        data = bytes(time.ctime(time.time()), 'utf-8')
        tam = s.send(data)
        print('sensor enviou ',tam, 'bytes')
        print(data)
    else:
        print('comando desconhecido: ', data)
    
    