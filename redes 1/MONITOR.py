#!/usr/bin/env python3
import socket
import sys
import threading

#--------------------------------------------------------------
# FUNÇÕES

def TrataSensor(conn, addr):

  print('Uma thread foi criada para:', addr)

  # O sensor deve enviar seu ID apos a conexao
  sensor = conn.recv(10)#o 10 representa a quantidade de bytes que será recebido.
  SENSORES[sensor] = conn

  print('sensor ', sensor, ' registrado no socket', conn)
   
  # CONSULTA é uma mensagem do protocolo de aplicação
  # ... é necessario transformar uma string em bytes antes de transmitir

  conn.send(bytes('CONSULTA','utf-8'))
  while True:
        data = conn.recv(100)
        print('sensor ', sensor, 'enviou ', data)
 
        if not data:
            break
       
  conn.close()     
  print('O sensor', sensor, 'encerrou')

#--------------------------------------------------------------
# PROGRAMA PRINCIPAL

HOST = '127.0.0.1'               # ANY_IP = todos os IPs do HOST
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
    print('recebi uma conexao do sensor ', addr)

    t = threading.Thread( target=TrataSensor, args=(conn,addr,))
    t.start()
#--------------------------------------------------------------

print('o servidor encerrou')
s.close()