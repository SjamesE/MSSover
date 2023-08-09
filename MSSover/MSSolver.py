from pyautogui import *
import pyautogui
import keyboard
import win32api, win32con

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.154)

startX = 612#742
startY = 322


# Normal
# Expert: 30 16
cellNRx = 30
cellNRy = 16

os.system('mode ' + str(cellNRx * 2 + 2) + ',' + str(cellNRy * 2 + 2))

sizeCell = 30
szx = sizeCell * cellNRx
szy = sizeCell * cellNRy

grid = ["                              " for x in range(cellNRy)]
justStarted = True

def replaceChar(s, x, c):
    ss = list(s)
    ss[x] = c
    return "".join(ss)

def countUnknown(x, y):
    positions = []
    for yOffset in range(-1, 2):
        for xOffset in range(-1, 2):
            if yOffset == 0 and xOffset == 0: continue;
            if x + xOffset > -1 and x + xOffset < cellNRy and y + yOffset > -1 and y + yOffset < cellNRx:
                if grid[x + xOffset][y + yOffset] == "█":
                    positions.append(x + xOffset)
                    positions.append(y + yOffset)
    return positions

def countBombs(x, y):
    positions = []
    for yOffset in range(-1, 2):
        for xOffset in range(-1, 2):
            if yOffset == 0 and xOffset == 0: continue
            if x + xOffset > -1 and x + xOffset < cellNRy and y + yOffset > -1 and y + yOffset < cellNRx:
                if grid[x + xOffset][y + yOffset] == '▒':
                    positions.append(x + xOffset)
                    positions.append(y + yOffset)
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

    for x in range(cellNRx):
        for y in range(cellNRy):

            char = grid[y][x]

            # don't search if empty/unknown/mine
            if char == '█' or char == '0' or char == '▒': continue
                #print(str(y) + ", " + str(x) + "(" + char + ")" + " is empty/unknown/mine. Continuing...")
            
            unknownAround = countUnknown(y, x)
            bombsAround = countBombs(y, x)
            #print(str(y) + ", " + str(x) + "(" + char + ")" + " has " + str(len(pos)/2) + " unknown tiles around it and " + str(len(bmb)/2) + " mines.")
            
            cont = True
            for i in range(1, 8):

                if cont == False: continue

                if char == str(i):

                    # No of bomb around equals curr nr
                    if len(bombsAround) == i * 2:

                        if len(unknownAround) > 0:
                            xPos = unknownAround[0]
                            yPos = unknownAround[1]

                    elif (len(bombsAround) + len(unknownAround)) / 2 == i:

                        for j in range(0, len(unknownAround), 2):

                            grid[unknownAround[j]] = replaceChar(grid[unknownAround[j]], unknownAround[j+1], '▒')

                    cont = False

    return (xPos, yPos)
    #empties = [[countUnknown(y, x) for x in range(cellNRx)] for y in range(cellNRy)]
    ##print(empties) 
    #bombs = [countBombs(y, x) for x in range(cellNRx) for y in range(cellNRy)]
    #
    #for y in range(cellNRy):
    #    for x in range(cellNRx):
    #        nrXY = strs[y][x]
    #        if len(empties[y][x]) != 0:
    #            for yy in range(-1, 2):
    #                for xx in range(-1, 2):
    #                    if yy == 0 and xx == 0: continue;
    #                    if x + xx > -1 and x + xx < cellNRx and y + yy > -1 and y + yy < cellNRy and strs[y + yy][x + xx] != '▒' and strs[y + yy][x + xx] != '█':
    #                        if int(strs[y + yy][x + xx]) > 0:
    #                            nrXXYY = strs[yy][xx]
    #                            unkXY = empties[y][x]
    #                            unkXXYY = empties[yy][xx]
    #                            if nrXY == nrXXYY:
    #                                if math.fabs(len(unkXY) - len(unkXXYY)) == 2:
    #                                    return findNotCommonElement(unkXY, unkXXYY)
                                #elif nrXY + 1 == nrXXYY:
                                #    twoC1n = twoCommon1Not(unkXY, unkXXYY)
                                #    if twoC1n != -1:
                                #        return twoC1n


# +----------------------------------------+ MAIN +----------------------------------------+
paused = False
justPressedE = False

while keyboard.is_pressed('q') == False:

    # if just started, then wait for user to start
    if justStarted == True:
        while keyboard.is_pressed('`') == False:
            pass

    if keyboard.is_pressed('e'):
        if not(justPressedE):
            paused = not(paused)
            justPressedE = True
    else:
        justPressedE = False

    if paused: continue

    pic = pyautogui.screenshot(region=(startX, startY, szx, szy))
    #pic.save(r"C:\Users\jsovea\source\repos\MSSover\pic.png")
    
    # Data Reset Loop
    for y in range(0, cellNRy):
        for x in range(0, cellNRx):

            if justStarted == False:
                if grid[y][x] == '▒': continue

            r,g,b = pic.getpixel((x * sizeCell, y * sizeCell))
            #print(str(r) + " " + str(g) + " " + str(b), end = ' ')
            found = False

            if r == 255 and g == 255 and b == 255:
                #print(str(y) + " " + str(x))
                grid[y] = replaceChar(grid[y], x, '█')
            else:
                for yy in range(5, sizeCell - 10):
                    if found == True: continue
                    for xx in range(5, sizeCell - 10):
                        #print(str(x + xx) + " " + str(y + yy), end = ": ")
                        #print(str(r) + " " + str(g) + " " + str(b))
                        if found == True: continue
                        r,g,b = pic.getpixel((x  * sizeCell + xx, y  * sizeCell + yy))
                        if r == 0 and g == 0 and b == 255:
                            grid[y] = replaceChar(grid[y], x, '1')
                            found = True
                        elif r == 0 and g == 128 and b == 0:
                            grid[y] = replaceChar(grid[y], x, '2')
                            found = True
                        elif r == 255 and g == 0 and b == 0:
                            grid[y] = replaceChar(grid[y], x, '3')
                            found = True
                        elif r == 0 and g == 0 and b == 128:
                            grid[y] = replaceChar(grid[y], x, '4')
                            found = True
                        elif r == 128 and g == 0 and b == 0:
                            grid[y] = replaceChar(grid[y], x, '5')
                            found = True
                        elif r == 0 and g == 128 and b == 128:
                            grid[y] = replaceChar(grid[y], x, '6')
                            found = True
                        elif r == 0 and g == 0 and b == 0:
                            grid[y] = replaceChar(grid[y], x, '7')
                            found = True
                        elif r == 128 and g == 128 and b == 128:
                            grid[y] = replaceChar(grid[y], x, '8')
                            found = True
                if found == False:
                    grid[y] = replaceChar(grid[y], x, '0')
                    #print("Empty")
            #else: print("huh??")

    os.system('cls')
    justStarted = False
    
    for i in range(cellNRy):

        print('+' + "-+" * cellNRx)
        
        for j in range(len(grid[i])):
            print('|' + str(grid[i][j]), end='')
        
        print('|')

    print('+' + "-+" * cellNRx)
        
    y,x = getNextPos()

    #while True:
    #    if keyboard.is_pressed('c'):
    #        time.sleep(0.5)
    #        break

    ######print(str(x) + " " + str(y))
    if (x != -1 and y != -1):
        click(startX + x * sizeCell + int(sizeCell/2), startY + y * sizeCell + int(sizeCell/2))

    if keyboard.is_pressed('r') == True:
        grid = ["                              " for x in range(cellNRy)]
    




    #for i in range(cellNRy):
    #    print(str(strs[i]))
    #
    #print("-----------------------")
    
    #while keyboard.is_pressed('1') == False:
    #    pass
    #while keyboard.is_pressed('`') == False:   
    #    pass
    
    #time.sleep(0.05)
