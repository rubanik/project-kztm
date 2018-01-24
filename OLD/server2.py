#-*- coding: utf-8 -*-
import socket
import pickle
import toexel
import sys
from _thread import *

host = ''
port = 5560



def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
        s.listen(10)

    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s


def setupConnection():

    # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(dataTransfer, (conn,))
    return conn

def reciveingData(dataMessage):
    print('Server: Отправляю ответ клиенту')
    conn.send(str.encode('OK'))
    print('Server: Принимаю список..')

    arr = conn.recv(1024)
    while arr is True:
         arr = conn.recv(1024)

    reply = 'Server: Список получен!'
    s = pickle.loads(arr)
    print('Server: Содержимое списка: ')
    for i in s:
        print(str(i))
    toexel.loadToExel(s)

    return reply

def transfer_command():
    data = conn.recv(1024)
    command = pickle.loads(data)
    return command





def dataTransfer(conn,):
    # A big loop that sends/receives data until told not to.

    while True:

        # Receive the data
        print('Server: Ожидаю запрос...')
        #data = conn.recv(1024)
        #data = data.decode()
        data = transfer_command()
        print('Server: Запрос получен и принят.')

        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'start':
            reply = reciveingData(dataMessage)
        elif command == 'pause':
            reply = reciveingData(dataMessage)
        elif command == 'continue':
            reply = reciveingData(dataMessage)

        elif command == 'exit':
            print("Our client has left us :(")
            break
        elif command == 'kill':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Command'
        # Send the reply back to the client
        conn.send(str.encode(reply))
        print("Server: Все данные успешно приняты!")
    conn.close()
    print('conn closed')

s = setupServer()



while True:
    #try:
        conn = setupConnection()
        #start_new_thread(dataTransfer(conn,))


    #except:
           #break
