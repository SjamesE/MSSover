from cmath import log
from itertools import count
import math
from subprocess import CREATE_NEW_CONSOLE
from tkinter.ttk import Sizegrip
from xml.etree import ElementInclude
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import random

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

startX = 739
startY = 315
cellNR = 9
sizeCell = 30
sz = sizeCell * cellNR
time.sleep(1)

strs = ["         " for x in range(cellNR)]
first = True

def replaceChar(s, x, c):
    ss = list(s)
    ss[x] = c
    return "".join(ss)

def countUnknown(x, y):
    positions = []
    for yy in range(-1, 2):
        for xx in range(-1, 2):
            if yy == 0 and xx == 0: continue;
            if x + xx > -1 and x + xx < cellNR and y + yy > -1 and y + yy < cellNR:
                if strs[x + xx][y + yy] == "?":
                    positions.append(x + xx)
                    positions.append(y + yy)
    return positions

def countBombs(x, y):
    positions = []
    for yy in range(-1, 2):
        for xx in range(-1, 2):
            if yy == 0 and xx == 0: continue
            if x + xx > -1 and x + xx < cellNR and y + yy > -1 and y + yy < cellNR:
                if strs[x + xx][y + yy] == 'x':
                    positions.append(x + xx)
                    positions.append(y + yy)
    return positions

def findNotCommonElement(a, b):
    if len(b) > len(a): c = a; a = b; b = c

    for i in range(0, len(a), 2):
        if (i < len(b)):
            if (a[i] == b[i] and a[i + 1] == b[i + 1]): continue
        return a[i],a[i + 1]

def getNextPos():
    xPos = -1
    yPos = -1
    for y in range(cellNR):
        for x in range(cellNR):
            char = strs[x][y]
            if char == '?' or char == '0' or char == 'x': 
                print(str(x) + ", " + str(y) + "(" + char + ")" + " is empty/unknown/mine. Continuing...")
                continue
            
            pos = countUnknown(x, y)
            bmb = countBombs(x, y)
            print(str(x) + ", " + str(y) + "(" + char + ")" + " has " + str(len(pos)/2) + " unknown tiles around it and " + str(len(bmb)/2) + " mines.")
            
            cont = True
            for i in range(1, 8):
                if cont == False: continue
                if char == str(i):
                    if len(bmb) == i * 2:
                        if len(pos) > 0:
                            xPos = pos[0]
                            yPos = pos[1]
                    elif (len(bmb) + len(pos)) / 2 == i:
                        for j in range(0, len(pos), 2):
                            strs[pos[j]] = replaceChar(strs[pos[j]], pos[j+1], 'x')
                    cont = False

    empties = [[countUnknown(y, x) for x in range(cellNR)] for y in range(cellNR)]
    #print(empties)
    #bombs = [countBombs(y, x) for x in range(cellNR) for y in range(cellNR)]

    for y in range(cellNR):
        for x in range(cellNR):
            nrXY = strs[y][x]
            if len(empties[y][x]) != 0:
                for yy in range(-1, 2):
                    for xx in range(-1, 2):
                        if yy == 0 and xx == 0: continue;
                        if x + xx > -1 and x + xx < cellNR and y + yy > -1 and y + yy < cellNR and strs[y + yy][x + xx] != 'x' and strs[y + yy][x + xx] != '?':
                            if int(strs[y + yy][x + xx]) > 0:
                                nrXXYY = strs[yy][xx]
                                unkXY = empties[y][x]
                                unkXXYY = empties[yy][xx]
                                if nrXY == nrXXYY:
                                    if math.abs(len(unkXY) - len(unkXXYY) == 2:
                                        return findNotCommonElement(unkXY, unkXXYY)
                                elif nrXY + 1 == nrXXYY
                                    twoC1n = twoCommon1Not(unkXY, unkXXYY)
                                    if twoC1n != -1:
                                        return twoC1n

                                    

    return (xPos, yPos)

while keyboard.is_pressed('q') == False:
    if first == True:
        while keyboard.is_pressed('`') == False:
            pass

    pic = pyautogui.screenshot(region=(startX, startY, sz, sz))
    pic.save(r"C:\Users\jsovea\source\repos\MSSover\pic.png")
    
    for y in range(0, cellNR):
        for x in range(0, cellNR):
            if first == False:
                if strs[y][x] != '?': continue
            r,g,b = pic.getpixel((x * sizeCell, y * sizeCell))
            #print(str(r) + " " + str(g) + " " + str(b), end = ' ')
            found = False
            if r == 255 and g == 255 and b == 255:
                strs[y] = replaceChar(strs[y], x, '?')
                #print("Unknown")
            else:
                for yy in range(5, sizeCell - 10):
                    if found == True: continue
                    for xx in range(5, sizeCell - 10):
                        #print(str(x + xx) + " " + str(y + yy), end = ": ")
                        #print(str(r) + " " + str(g) + " " + str(b))
                        if found == True: continue
                        r,g,b = pic.getpixel((x  * sizeCell + xx, y  * sizeCell + yy))
                        if r == 0 and g == 0 and b == 255:
                            strs[y] = replaceChar(strs[y], x, '1')
                            found = True
                        elif r == 0 and g == 128 and b == 0:
                            strs[y] = replaceChar(strs[y], x, '2')
                            found = True
                        elif r == 255 and g == 0 and b == 0:
                            strs[y] = replaceChar(strs[y], x, '3')
                            found = True
                        elif r == 0 and g == 0 and b == 128:
                            strs[y] = replaceChar(strs[y], x, '4')
                            found = True
                        elif r == 128 and g == 0 and b == 0:
                            strs[y] = replaceChar(strs[y], x, '5')
                            found = True
                        elif r == 0 and g == 128 and b == 128:
                            strs[y] = replaceChar(strs[y], x, '6')
                            found = True
                        elif r == 0 and g == 0 and b == 0:
                            strs[y] = replaceChar(strs[y], x, '7')
                            found = True
                        elif r == 128 and g == 128 and b == 128:
                            strs[y] = replaceChar(strs[y], x, '8')
                            found = True
                if found == False:
                    strs[y] = replaceChar(strs[y], x, '0')
                    #print("Empty")
            #else: print("huh??")

    
    first = False

    for i in range(cellNR):
        print(str(strs[i]))
        
    y,x = getNextPos()
    print(str(x) + " " + str(y))
    click(startX + x * sizeCell + int(sizeCell/2), startY + y * sizeCell + int(sizeCell/2))
    
    for i in range(cellNR):
        print(str(strs[i]))

    #while keyboard.is_pressed('`') == False:
    #    pass
    
    #time.sleep(0.05)
