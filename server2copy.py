#-*- coding: utf-8 -*-
import socket
import pickle
import toexel
import sys
from _thread import *
import threading
import multiprocessing

host = ''
port = 5560



def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))

    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s


def setupConnection():

    # Allows one connection at a time.
    print("here")
    conn, address = s.accept()
    print('tuta')
    print("Connected to: " + address[0] + ":" + str(address[1]))
    #start_new_thread(dataTransfer, (conn,))
    connthread = threading.Thread(target=dataTransfer, args=(conn,))
    connthread.start()
    return conn

def reciveingData(dataMessage):
    print('Server: Отправляю ответ клиенту')
    conn.send(str.encode('OK'))
    print('Server: Принимаю список..')

    arr = conn.recv(1024)
    while arr is True:
         arr = conn.recv(1024)

    reply = 'Server: Список получен! От' + str(conn.getsockname())
    s = pickle.loads(arr)
    print('Server: Содержимое списка: ')
    for i in s:
        print(str(i))
    toexel.loadToExel(s)

    return reply


def transfer_to_client(reply):
    rawreply = pickle.dumps(reply)
    conn.send(rawreply)




def transfer_command():
    print(multiprocessing.current_process().name + ' in transfer')
    data = conn.recv(1024)
    command = pickle.loads(data)
    print(multiprocessing.current_process().name + "after pickle")
    return command

def recieving_array():
    print(multiprocessing.current_process().name + 'in recv array')

    rawarray = conn.recv(1024)


    print(multiprocessing.current_process().name+ str(rawarray))
    array = pickle.loads(rawarray)
    print('Server: Список получен! От' + str(conn.getpeername()))
    print('Server: Содержимое списка: ')
    print(str(array))
    # for i in array:
    #     print(str(i))
    toexel.loadToExel(array)
    print('OK')
    reply = 'Список получен!'
    return reply




def dataTransfer(conn,adrr):
    # A big loop that sends/receives data until told not to.

    while True:

        # Receive the data
        print('Server: Ожидаю запрос... от ' + str(adrr))
        print(multiprocessing.current_process().name)
        #data = conn.recv(1024)
        #data = data.decode()
        data = transfer_command()
        print('Server: Запрос получен и принят.')

        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'start':
            #reply = reciveingData(dataMessage)
            reply = recieving_array()
        elif command == 'pause':
            reply = recieving_array()
        elif command == 'continue':
            reply = recieving_array()
        elif command == 'stop':
            reply = recieving_array()

        elif command == 'exit':
            print("Our client has left us :(")
            break
        elif command == 'kill':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'SERVER:Unknown Command'
        # Send the reply back to the client
            print(reply)
        #transfer_to_client(reply)
        print("Server: Все данные успешно приняты!")

    conn.close()

s = setupServer()

processes=[]

while True:
    try:
        s.listen(10)
        print("Ожидаю подключения")
        conn,adrr = s.accept()
        # threadLock = threading.Lock()
        # conThread = threading.Thread(target=dataTransfer, args=(conn,adrr))
        # conThread.start()
        proc = multiprocessing.Process(target=dataTransfer, args=(conn,adrr))
        proc.start()

        #conn = setupConnection()
        #start_new_thread(dataTransfer(conn,))

    except:
           break

