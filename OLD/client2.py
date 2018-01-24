#-*- coding: utf-8 -*-
import socket
import pickle
import datetime

#===================================================================================================


#Станок_________________________________________[0]
#Номер заказа___________________________________[1]
#Дата постановки на станок______________________[2]
#Время постановки на станок_____________________[3]
#Часы по нормеровке_____________________________[4]
#Планируемое время: Дата окончания обработки____[5]
#                   Время окончания обработки___[6]
#Фактическое время: Дата окончания обработки____[7]
#                   Время окончания обработки___[8]
#Оператор_______________________________________[9]
#Статус________________________________________[10]
#Прична простоя оборудования___________________[11]
#Простой начался:   Дата начала простоя________[12]
#                   Время начала простоя_______[13]
#Простой закончился: Дата конца простоя________[14]
#                    Время конца простоя_______[15]
#Общее время простоя___________________________[16]
#Фактическое время обработки___________________[17]

def arrCollect(cmd):

    dataTime = datetime.datetime.now()

    #Заполняем массив исходя из команды

    if command == 'start':

        #Указываем станок
        mach = machine
        myarray.append(mach)

        #Вводим номер заказа
        orderName = get_currentOrder()
        myarray.append(orderName)

        dataInst = datetime.date.strftime(dataTime,'%d.%m.%y')               #Текущая дата
        timeInst = datetime.date.strftime(datetime.datetime.now(),'%H:%M:%S')#Текущее время
        myarray.append(dataInst)
        myarray.append(timeInst)
        #Добавляем время начала в список для расчета времени всей работы
        mytimearray.append(dataTime)

        #Вводим нормировку
        normTime = get_currentNorm()
        myarray.append(normTime)


        #Расчитываем плановую дату
        pdate = dataTime + datetime.timedelta(hours=int(normTime))

        planDate = datetime.date.strftime(pdate, '%d.%m.%y' ) #планируемая дата
        planTime = datetime.date.strftime(pdate,'%H:%M:%S') #планируемое время

        myarray.append(planDate)
        myarray.append(planTime)


        factDate = '-'
        factTime = '-'

        myarray.append(factDate)
        myarray.append(factTime)

        #Вводим имя
        operatorName = get_currentUser()
        myarray.append(operatorName)

        state = get_currentState(cmd)
        myarray.append(state)

        myarray.append(' ')
        myarray.append(' ')
        myarray.append(' ')
        myarray.append(' ')
        myarray.append(' ')
        myarray.append(' ')
        myarray.append(' ')


        arr = myarray

        return arr

    #Заполнение массива при постановке на паузу по какой либо причине(Причина указывается)
    elif command == 'pause':
        tempArr = myarray.copy()


        for i in range(len(tempArr)):
            tempArr[i] = '-'

        tempArr[0] = machine
        tempArr[1] = myarray[1]
        tempArr[9] = myarray[9]
        tempArr[10] = get_currentState(cmd)
        myarray[10] = tempArr[10]
        tempArr[11] = input('Причина простоя: ')
        tempArr[12] = datetime.date.strftime(dataTime,'%d.%m.%y')
        myarray[12] = datetime.datetime.now()
        tempArr[13] = datetime.date.strftime(datetime.datetime.now(),'%H:%M:%S')

        return tempArr

    elif command == 'continue':


        #Копируем исходный массив
        tempArr = myarray.copy()
        #Заполняем прочерками
        for i in range(len(tempArr)):
             tempArr[i] = '-'

        tempArr[0] = machine
        tempArr[1] = myarray[1]
        tempArr[9] = myarray[9]#Сделать проверку на пересменок
        tempArr[10] = get_currentState(cmd)
        myarray[10] = tempArr[10]
        tempArr[14] = datetime.date.strftime(dataTime, '%d.%m.%y')
        tempArr[15] = datetime.date.strftime(datetime.datetime.now(), '%H:%M:%S')

        #delta = datetime.timedelta(days= int(myarray[12].day), hours = myarray[12].hour, minutes=myarray[12].minute,
        #                           seconds=myarray[12].second)
        #print(delta)

        delta = dataTime - myarray[12]
        days = delta.days
        hours = delta.seconds//3600
        minutes = (delta.seconds%3600)//60
        print( str(hours)+":"+str(minutes) )

        p = int(delta.days) - int(dataTime.day)
        #ДАТА - ДАТА , а потом берем из дельты количество минут!
        tempArr[16] = '%02d:%02d' % (hours,minutes)
        print (tempArr[16])

        return tempArr

    elif command == 'stop':
        tempArr = myarray.copy()


        for i in range(len(tempArr)):
            tempArr[i] = '-'

        tempArr[0]= machine
        tempArr[1]= myarray[1]
        tempArr[7] = datetime.date.strftime(dataTime, '%d.%m.%y')
        tempArr[8] = datetime.date.strftime(datetime.datetime.now(), '%H:%M:%S')
        tempArr[9]= myarray[9]
        tempArr[11]= get_currentState(cmd)

        #Так как дата установки это стринг, сделать список с хранилищем времени в формате Date.
        #в который при старте будет заносится объект, а при стопе использоваться для вычисления
        #фактической даты окончания. Потом этот лист необходимо будет очищать вместе с основным.

        finishdelta = dataTime - mytimearray
        hours = finishdelta.seconds // 3600
        minutes = (finishdelta.seconds % 3600) // 60
        tempArr[17] = tempArr[16] = '%02d:%02d' % (hours,minutes)

        return tempArr



#===================================================================================================

def sendingData(arr):
    g = pickle.dumps(arr)
    print('Client: Отправка запроса.')
    reply1 = s.send(str.encode(command))

    while reply1 is True:
        reply1 = s.send(g)
    print('Client: Запрос отправлен.')
    reply = s.recv(1024)
    if (reply.decode('utf-8')) == 'OK':
        reply = s.send(g)
        while reply is True:
            reply = s.send(g)
        print('Client: Список отправлен.')
        reply = s.recv(1024)
        print(reply.decode('utf-8'))

def collect_and_send(cmd):
    arr_to_send = arrCollect(cmd)
    sendingData(arr_to_send)

def get_currentUser():
    cu = input('Оператор :')
    return cu
def get_currentOrder():
    co = input('Номер заказа: ')
    order = co
    return co
def get_currentState(cmd):
    if cmd == 'start':
        return 'В работе'
    elif cmd == 'pause':
        return 'Простой'
    elif cmd == 'stop':
        return 'Закончен'
    elif cmd == 'continue':
        return 'Работа возобновлена'

    else:
        return 'whats wrong?'
def get_currentNorm():
    cn = input('Нормировка в часах: ')
    return cn



machine ='ДИП-500'

host = '127.0.0.1'
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

myarray=[]
mytimearray=[]

while True:

    command = input("Введите команду: ")
    if command == 'exit':
        #send EXIT request to other end
        s.send(str.encode(command))
        break
    elif command == 'kill':
        s.send(str.encode(command))
        break

    elif command == 'start':
        if myarray != []:
            print('Работа в процессе!')
        else:
            collect_and_send(command)

    elif command == 'pause':
        if myarray == []:
            print('Нет активной работы!')
        elif myarray != [] and myarray[10]=='Простой'  :
            print('Есть актвный простой!')
        else:
             collect_and_send(command)

    elif command == 'continue':
        if myarray == [] or myarray[10]=='В работе':
            print('Нет активного простоя!')
        elif myarray != [] and myarray[10]=='Работа возобновлена':
            print('Работа уже возобновлена!')
        else:
             collect_and_send(command)

    elif command == 'stop':
        if myarray == []:
            "Нет активной работы"
        elif myarray[10] == "Простой":
            "Завершите активный простой!"
        else:
            collect_and_send(command)


    else:
        s.send(str.encode(command))
        reply = s.recv(1024)
        print(reply.decode('utf-8'))



s.close()
