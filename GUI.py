# -*- coding: utf-8 -*-

import tkinter as tk
import socket
import client2copy
#####
#Название станка
NAME_OF_MACHINE = "ДИП-500"


def start_operation(event):
    client2copy.aaa = 'start'

def start_connection(host, port,sock ):
    sock.connect((host, port))
    print('Подключен к : ' + str(sock.getpeername()))
    listLog.insert("end",'Подключен к : ' + str(sock.getpeername()))
    client2copy.client_processes(sock)

def acceptData(event):
    operator = var.get()
    order = textOrder.get()
    norm = textOrder1.get()
    if operator != "Выбрать..." and str.isdigit(order) and str.isdigit(norm):
        allDataList[1] = operator
        allDataList[2] = order
        allDataList[3] = norm
        dataWindow.withdraw()
        startButton.config(state="normal")
        listLog.insert('end','Данные приняты! Оператор: %s, Заказ: %s, Время на исполнение: %s.'% (str(operator),str(order),str(norm)))
        print(allDataList)
    if operator == "Выбрать...":
        optMenu.configure(bg='pink')
    else:
        optMenu.configure(bg='lightgreen')
    if str.isdigit(order)==False:
        textOrder.configure(bg='pink')
    else:
        textOrder.configure(bg='lightgreen')
    if str.isdigit(norm)==False:
        textOrder1.configure(bg='pink')
    else:
        textOrder1.configure(bg='lightgreen')

def start(event):
    print('BOOM')
   # collect_array(cmd, arr)

#Тут мы создаем и заполняем основной список данных пустыми полями
x=''
allDataList= [x for i in range(13)]
allDataList[0] = NAME_OF_MACHINE
print(allDataList)


#Главное окно
root = tk.Tk()
#Титульник
root.title("Программа контроля производительности")
root.geometry("800x600+100+100")

#Окно ввода данных
dataWindow = tk.Toplevel()
dataWindow.title("Ввод данных обратотки")
dataWindow.geometry("500x200+250+300")
dataWindow.attributes('-topmost', 'true')
dataWindow.overrideredirect(1)
#Заполнение окна
#Operator
operatorDataL = tk.LabelFrame(dataWindow,text = 'Оператор', width =265,height=60)
operatorDataL.place(x=10,y=10)
var = tk.StringVar()
var.set("Выбрать...")
optMenu = tk.OptionMenu(operatorDataL, var , 'Иванов Иван Иванович',"Петров Василий Дмитриевич", "Сидоров Гальфитеп Фарухович")
optMenu.place(x=5,y=5)
optMenu.configure(width= 26)
orderNumberL = tk.LabelFrame(dataWindow,text = 'Номер заказа', width =265,height=60)
orderNumberL.place(x=10,y=70)
textOrder = tk.Entry(orderNumberL,width=24, font='Helvetica, 14',justify='center')
textOrder.place(x=7,y=5)
timeNormL = tk.LabelFrame(dataWindow,text = 'Время на обработку', width =265,height=60)
timeNormL.place(x=10,y=130)
textOrder1 = tk.Entry(timeNormL,width=24, font='Helvetica, 14',justify='center')
textOrder1.place(x=7,y=5)
buttonAccept = tk.Button(dataWindow, width=23,height=11, text = 'Принять')
buttonAccept.place(x=280,y=19)

buttonAccept.bind('<Button-1>',acceptData)




conn_FLAG = False
host = '127.0.0.1'
port = 5560


menu = tk.Menu(root)
root.config(menu=menu)
cmd = ''
#root.wm_attributes('-alpha',0.5) #прозрачность



submenu1 = tk.Menu(menu)
menu.add_cascade(label='First', menu=submenu1 )
submenu1.add_cascade(label='One')
submenu1.add_cascade(label='Two')
submenu1.add_cascade(label='Three')

submenu2 = tk.Menu(menu)
menu.add_cascade(label='Second', menu=submenu2 )
submenu2.add_cascade(label='One')
submenu2.add_cascade(label='Two')
submenu2.add_cascade(label='Three')

submenu3 = tk.Menu(menu)
menu.add_cascade(label='Thirst', menu=submenu3 )
submenu3.add_cascade(label='One')
submenu3.add_cascade(label='Two')
submenu3.add_cascade(label='Three')
###############################################################
#               ТАБЛИЧКА С НАЗВАНИЕМ СТАНКА                #
###############################################################


frameStanokName = tk.LabelFrame(root,
                                text="Станок",
                                labelanchor = 'nw',
                                width =248,
                                height = 71
                                )

label0 = tk.Label(frameStanokName,
                  text = NAME_OF_MACHINE,

                  anchor='center',
                  font = "Times, 20",

                  )

###############################################################
#               ТАБЛИЧКА С ДАННЫМИ О ПОДКЛЮЧЕНИИ              #
###############################################################
# labelConnData = tk.LabelFrame(root,
#                            text="Connection info",
#                            labelanchor = 'nw',
#                            width =30)
# print(labelConnData.winfo_width(),labelConnData.winfo_height())
# label3 = tk.Label(labelConnData,
#                text = "Connected to: "+s3,
#                width = 30,
#                anchor='w',
#                justify='left',
#                font = "Times, 10")
# label4 = tk.Label(labelConnData,
#                text = "Current time: "+s4 ,
#                width = 30,
#                anchor='w',
#                justify = 'left',
#                font = "Times, 10")
# #frame = tk.Frame(root, width = 100,height=100)
###############################################################
#               ТАБЛИЧКА С ДАННЫМИ О СОСТОЯНИИ                #
###############################################################

stateFrame = tk.LabelFrame(root,
                           text="Текущее состояние",
                           labelanchor = 'nw',
                           width =258,
                           height =71)

stateLabel = tk.Label(stateFrame,
               text = 'Готов к работе',

               anchor='w',
               justify = 'left',
               font = "Times, 20")


###############################################################
#               ОКНО ДЛЯ ЛОГОВ И ОПИСАНИЯ ПРОЦЕССА            #
###############################################################
logFrame = tk.LabelFrame(root,
                           text='INFORMATION',
                           labelanchor = 'nw',
                           width =780,
                           height =165)

listLog = tk.Listbox(logFrame, width=95, height=9,bg="gray")
logScr = tk.Scrollbar(listLog,command=listLog.yview,relief='groove')
listLog.configure(yscrollcommand=logScr.set)
listLog.selection_set(first=0,last=1)
###############################################################
#               ТАБЛИЧКА С ДАННЫМИ О СОСТОЯНИИ                #
###############################################################

timerFrame = tk.LabelFrame(root,
                           text="Таймер рабочего времени",
                           labelanchor = 'nw',
                           width =248,
                           height =71)

timerLabel = tk.Label(timerFrame,
               text = 'Тик тик тик',
               width = 30,
               anchor='w',
               justify = 'left',
               font = "Times, 10")

###############################################################
#         ОБЛАСТЬ C ДАННЫМИ
###############################################################

mainDataFrame = tk.LabelFrame(root,
                           text="Рабочие данные",
                           labelanchor = 'nw',
                           width =517,
                           height =322)

###############################################################
#         ОБЛАСТЬ С КНОПКОЙ СТАРТ
###############################################################

startButtonFrame = tk.LabelFrame(root,

                           labelanchor = 'nw',
                           width =248,
                           height =71,)
startButton = tk.Button(startButtonFrame,text = 'НАЧАТЬ',width = 25, height = 3,state='disabled')

###############################################################
#         ОБЛАСТЬ С КНОПКОЙ PAUSE
###############################################################

pauseButtonFrame = tk.LabelFrame(root,

                           labelanchor = 'nw',
                           width =248,
                           height =71)
pauseButton = tk.Button(pauseButtonFrame,text = 'ПРИОСТАНОВИТЬ',width = 25, height = 3,state='disabled')


###############################################################
#         ОБЛАСТЬ С КНОПКОЙ CONTINUE
###############################################################

contButtonFrame = tk.LabelFrame(root,

                           labelanchor = 'nw',
                           width =248,
                           height =71)
contButton = tk.Button(contButtonFrame,text = 'ПРОДОЛЖИТЬ',width = 25, height = 3,state='disabled')

###############################################################
#         ОБЛАСТЬ С КНОПКОЙ STOP
###############################################################

stopButtonFrame = tk.LabelFrame(root,

                           labelanchor = 'nw',
                           width =248,
                           height =71)
stopButton = tk.Button(stopButtonFrame,text = 'ЗАКОНЧИТЬ',width = 25, height = 3,state='disabled')

################################################
#ВРЕМЕННОЕ ЗАПОЛНЕНИЕ ЛОГА
# x=0
# for i in range(len(testList)):
#     listLog.insert("end",testList[i]+' '+str(x))
#     x=x+1
#################################################

#######################################
#  ОСНОВНЫЕ ДАННЫЕ
frameStanokName.place(x=10, y=10)
label0.place(x = 75,y = 10)

########################################
#  СОСТОЯНИЕ
stateFrame.place(x=270,y=10)
stateLabel.place(x = 35,y = 10)

#########################################
# TIMER
timerFrame.place(x = 541, y =10)
timerLabel.place(x=0,y=0)

#########################################
#  MAIN DATA

mainDataFrame.place(x=10, y=91)
#########################################
# LOG
logFrame.place(x=10, y=425)
listLog.place(x=7, y=3)
logScr.place(relx=1,rely=0,relheight=1,bordermode="inside",anchor='ne')

##########################################
# start button
startButtonFrame.place(x=541, y = 98)
startButton.place(x = 8,y=5)
startButton.bind('<Button-1>',start)

##########################################
# pause button
pauseButtonFrame.place(x=541, y = 179)
pauseButton.place(x = 8,y=5)

##########################################
# continue button
contButtonFrame.place(x=541, y = 260)
contButton.place(x = 8,y=5)

##########################################
# stop button
stopButtonFrame.place(x=541, y = 341)
stopButton.place(x = 8,y=5)


#startButton.bind('<Button-1>', start_operation)
root.update_idletasks()




root.mainloop()