import math
from pyautogui import *
import pyautogui
import keyboard
import win32api, win32con

def click(x, y):
    win32api.SetCursorPos((x, y))
    if _click:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.01)

startX = 612#742
startY = 322

# Normal
# Expert: 30 16
noOfColumns = 30
noOfRows = 16

os.system('mode ' + str(noOfColumns * 2 + 3) + ',' + str(noOfRows * 2 + 4))

sizeCell = 30
szx = sizeCell * noOfColumns
szy = sizeCell * noOfRows

grid = ["                              " for x in range(noOfRows)]
justStarted = True

def replaceChar(_list, offset, char):
    ss = list(_list)
    ss[offset] = char
    return "".join(ss)

def countUnknown(x, y):
    positions = []
    for yOffset in range(-1, 2):
        for xOffset in range(-1, 2):
            if yOffset == 0 and xOffset == 0: continue;
            if x + xOffset > -1 and x + xOffset < noOfRows and y + yOffset > -1 and y + yOffset < noOfColumns:
                if grid[x + xOffset][y + yOffset] == "█":
                    positions.append(x + xOffset)
                    positions.append(y + yOffset)
    return positions

def countBombs(x, y):
    positions = []
    for yOffset in range(-1, 2):
        for xOffset in range(-1, 2):
            if yOffset == 0 and xOffset == 0: continue
            if x + xOffset > -1 and x + xOffset < noOfRows and y + yOffset > -1 and y + yOffset < noOfColumns:
                if grid[x + xOffset][y + yOffset] == '▒':
                    positions.append(x + xOffset)
                    positions.append(y + yOffset)
    return positions

def findAround1stButNot2nd(list1, list2, sort):
    if sort:
        if len(list2) > len(list1): 
            c = list1
            list1 = list2
            list2 = c

    for i in range(0, len(list1), 2):
        found = False
        for j in range(0, len(list2), 2):

            if list1[i] != list2[j] or list1[i+1] != list2[j+1] : continue
            found = True

        if found == False:
            return (list1[i], list1[i+1])

    return (-1, -1)

# check if all squares are common except one, and return that one square. ERR -> (-1, -1)
def allCommonExceptOne(list1, list2):

    if len(list2) > len(list1): 
            c = list1
            list1 = list2
            list2 = c

    notCommon = (-1, -1)
    
    for i in range(0, len(list1), 2):
        found = False
        for j in range(0, len(list2), 2):

            if list1[i] == list2[j] and list1[i+1] == list2[j+1]:
                found = True
                break

        if not(found):
            if notCommon == (-1, -1):
                notCommon = (list1[i], list1[i+1])
            else:
                return (-1, -1)

    return notCommon

def getNextPos():
    xPos = -1
    yPos = -1

    for x in range(noOfColumns):
        for y in range(noOfRows):

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
                            return (unknownAround[0], unknownAround[1])

                    elif (len(bombsAround) + len(unknownAround)) / 2 == i:

                        for j in range(0, len(unknownAround), 2):

                            grid[unknownAround[j]] = replaceChar(grid[unknownAround[j]], unknownAround[j+1], '▒')

                    cont = False
    
    if not(keyboard.is_pressed('w')):
        return (-1, -1)

    empties = [[countUnknown(y, x) for x in range(noOfColumns)] for y in range(noOfRows)]
    #print(empties) 
    
    for y in range(noOfRows):
        for x in range(noOfColumns):

            nrXY = grid[y][x]
            if nrXY == '█' or nrXY == '0' or nrXY == '▒': continue

            if len(empties[y][x]) == 0: continue

            #if x == 22 and y == 11:
            #    _ = 1

            for yOffset in range(-1, 2):
                for xOffset in range(-1, 2):
                    if yOffset == 0 and xOffset == 0: continue
                    if math.fabs(yOffset) == math.fabs(xOffset): continue

                    yWithOffset = y + yOffset
                    xWithOffset = x + xOffset

                    # check out of bounds
                    if not(xWithOffset > -1          and
                           xWithOffset < noOfColumns and
                           yWithOffset > -1          and
                           yWithOffset < noOfRows ): continue

                    nrAtOffset = grid[yWithOffset][xWithOffset]

                    # continue if unknown or mine or 0
                    if nrAtOffset == '▒' or nrAtOffset == '█' or nrAtOffset == '0' : continue

                    # continue if 0
                    if int(grid[yWithOffset][xWithOffset]) <= 0: continue

                    unkXY  = empties[y][x]
                    unkAtOffset = empties[yWithOffset][xWithOffset]

                    nrXYNoBombs       = int(nrXY)       - len(countBombs(y, x))/2
                    nrAtOffsetNoBombs = int(nrAtOffset) - len(countBombs(yWithOffset, xWithOffset))/2

                    if nrXYNoBombs == 0 or nrAtOffsetNoBombs == 0: continue
                    #if nrXYNoBombs + len(unkXY) / 2 != int(nrXY) + 1 and nrAtOffsetNoBombs + len(unkAtOffset) / 2 != int(nrAtOffset) + 1: continue
                #    if len(unkXY) != 4 and len(unkAtOffset) != 4: continue #????????????????
                    
                    # if the 2 tiles have the same nr of bombs around (NOT FOUND)
                    if nrXYNoBombs == nrAtOffsetNoBombs: #last commented next line and added this one !!!!!!!!!!!!!
                    #if nrXYNoBombs == 1 and nrXYNoBombs == nrAtOffsetNoBombs:
                        if nrXYNoBombs == 1:
                            # if difference of unknown tiles is 1
                            if math.fabs(len(unkXY) - len(unkAtOffset)) == 2:
                                a = allCommonExceptOne(unkXY, unkAtOffset)
                                if a != (-1, -1):
                                    return a
                        elif True:
                            _ = 1 #continue here !!!!!!!!!!!!!!!

                    # if the difference of empty is 1
                    elif math.fabs(nrXYNoBombs - nrAtOffsetNoBombs) == 1:  
                        twoC1n = (-1, -1)
                    
                        if len(unkAtOffset)/2 == int(nrAtOffsetNoBombs) + 1:
                            twoC1n = allCommonExceptOne(unkAtOffset, unkXY)
                        elif len(unkXY)/2 == int(nrXYNoBombs) + 1:
                            twoC1n = allCommonExceptOne(unkXY, unkAtOffset)
                    
                        if twoC1n != (-1, -1):
                            #if grid[twoC1n[0], twoC1n[1]] == '█':
                            #    _ = 1
                            grid[twoC1n[0]] = replaceChar(grid[twoC1n[0]], twoC1n[1], '▒')

                    elif nrXYNoBombs == nrAtOffsetNoBombs:

                        if allFrom1stIn2ndRetIn2nd(unkXY, unkAtOffset)
                    
                #    # if the 2 tiles have the same nr of bombs around
                #    if nrXYNoBombs == 1 and nrXYNoBombs == nrAtOffsetNoBombs:
                #        # if difference of unknown tiles is 1
                #        if math.fabs(len(unkXY) - len(unkAtOffset)) == 2:
                #            a = findAround1stButNot2nd(unkXY, unkAtOffset, True)
                #            if a != (-1, -1):
                #                return a
                #            
                #    elif math.fabs(nrXYNoBombs - nrAtOffsetNoBombs) == 1:  
                #        twoC1n = (-1, -1)
                #
                #        if len(unkAtOffset)/2 == int(nrAtOffsetNoBombs) + 1:
                #            twoC1n = findAround1stButNot2nd(unkAtOffset, unkXY, False)
                #        elif len(unkXY)/2 == int(nrXYNoBombs) + 1:
                #            twoC1n = findAround1stButNot2nd(unkXY, unkAtOffset, False)
                #
                #        if twoC1n != (-1, -1):
                #            #if grid[twoC1n[0], twoC1n[1]] == '█':
                #            #    _ = 1
                #            grid[twoC1n[0]] = replaceChar(grid[twoC1n[0]], twoC1n[1], '▒')
                            

    return (-1, -1)


# +----------------------------------------+ MAIN +----------------------------------------+
paused = False
_click = False
justPressedE = False
justPressedF = False

#l1 = 5, 2, 5, 1, 6, 7, 1, 3, 7, 2, 6, 9
#l2 = 1, 3, 6, 7, 5, 1, 7, 2, 5, 2
#
#print(findNotCommonElement(l1, l2))

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

    if keyboard.is_pressed('f'):
        if not(justPressedF):
            _click = not(_click)
            justPressedF = True
    else:
        justPressedF = False

    pic = pyautogui.screenshot(region=(startX, startY, szx, szy))
    #pic.save(r"C:\Users\jsovea\source\repos\MSSover\pic.png")
    
    # Data Reset Loop
    for y in range(0, noOfRows):
        for x in range(0, noOfColumns):

            if justStarted == False:
                if grid[y][x] == '▒' : continue

            r,g,b = pic.getpixel((x * sizeCell, y * sizeCell))
            #print(str(r) + " " + str(g) + " " + str(b), end = ' ')
            found = False

            if r == 255 and g == 255 and b == 255:
                grid[y] = replaceChar(grid[y], x, '█')
                #print(str(y) + " " + str(x))
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

    #os.system('cls')
    justStarted = False
    
    print ('┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐')
    print ('│ │0│1│2│3│4│5│6│7│8│9│0│1│2│3│4│5│6│7│8│9│0│1│2│3│4│5│6│7│8│9│')
    for i in range(noOfRows):
        
        print('├' + "─┼" * noOfColumns + '─┤')
        print('│' + str(i%10), end='')
        for j in range(len(grid[i])):
            print('│' + str(grid[i][j]).replace('0', ' '), end='')
        
        print('│')

    print('└' + "─┴" * noOfColumns + '─┘')
    
    y,x = getNextPos()

    print('\033[91m' + '\033[' + str(4+y*2) + ';' + str(4+x*2) + 'HX' + '\033[0m')
    print('\033[35;0H└')
    

    #while True:
    #    if keyboard.is_pressed('c'):
    #        time.sleep(0.5)
    #        break

    ######print(str(x) + " " + str(y))
    if (x != -1 and y != -1):
        click(startX + x * sizeCell + int(sizeCell/2), startY + y * sizeCell + int(sizeCell/2))
    time.sleep(0.1)

    if keyboard.is_pressed('r') == True:
        grid = ["                              " for x in range(noOfRows)]
    




    #for i in range(cellNRy):
    #    print(str(strs[i]))
    #
    #print("-----------------------")
    
    #while keyboard.is_pressed('1') == False:
    #    pass
    #while keyboard.is_pressed('`') == False:   
    #    pass
    
    #time.sleep(0.05)
