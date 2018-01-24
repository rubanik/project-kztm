# -*- coding: utf-8 -*-

import openpyxl
import datetime





def loadToExel(list):
    filename = 'mywb.xlsx'


    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    wb.guess_types = True

    arr = list
    ws.append(arr)

    wb.save('mywb.xlsx')

    print('Download to exel Done!')
