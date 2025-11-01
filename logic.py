import random
import time

import colorama
from colorama import Fore

colorama.init(autoreset=True)

r1 = [0] * 7
r2 = [0] * 7
r3 = [0] * 7
r4 = [0] * 7
r5 = [0] * 7
r6 = [0] * 7
r7 = [0] * 7

box = [r1, r2, r3, r4, r5,r6,r7]

row = 0
col = 0
path = 1  # path of maze,the actual path
pathcount = 1  # to calc number of spaces filled
box[row][col] = 1
j_cr = []  # list of jumpable cells
jrow = 0 #jumped col
jcol = 0 #jumped row

RUN = True

while RUN:
    path_jump = False
    ncell = []  # options around the cell
    pre_row = row
    pre_col = col

    # checks all options around cell whether filled or not
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr != 0 and dc != 0:
                continue
            elif dr == 0 and dc == 0:
                continue

            nr = row + dr
            nc = col + dc

            if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
                if box[nr][nc] == 0:
                    ncell.append([nr, nc])

    print("original ncell : ", ncell)
    ori_ncell = ncell



    if not ncell: #if no options are available, ie, the cell path is stuck
        path_jump = True
        print("STUCK")
        for jcell in j_cr:
            jrow = jcell[0]
            jcol = jcell[1]
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 and dc != 0:
                        continue
                    elif dr == 0 and dc == 0:
                        continue

                    jr = jrow + dr
                    jc = jcol + dc

                    if 0 <= jr < len(box) and 0 <= jc < len(box[row]): #checks if options are inside grid
                        if box[jr][jc] == 0: # removes filled options from ncell and determines if stuck true or false
                            ncell.append([jr, jc])

            if ncell: #if the chosen jumpable cell has options around it to continue moving
                break
            else:
                print("tried ncell : ", ncell)

        print("new ncell : ", ncell)

    ocell = random.choice(ncell)
    row = ocell[0]
    col = ocell[1]

    # finds jumpable cells and adds them to list j_cr
    if len(ncell) > 1:
        j = list([pre_row, pre_col])
        j_cr.insert(0, j)

    print("ocell : ", ocell)
    print("j_cr : ", j_cr)


    if path_jump: #if a path had jumped, it retracks the path count
        path = box[jrow][jcol]

    path += 1
    box[row][col] = path
    pathcount += 1

#IGNORE, FOR CHECKING PATHWAY---------------------------------------
    for r in range(len(box)):
        for c in range(len(box[r])):

            if c == len(box[r])-1 and r == len(box)-1:
                c = box[r][c]
                c = str(c)
                if len(c) == 1:
                    print(" ", Fore.GREEN + c,"  ", end=' ')
                else:
                    print(' ',Fore.GREEN + c,' ', end='')

            elif c == 0 and r == 0:
                c = box[r][c]
                print(" ", Fore.RED + str(c),"  ",end='')

            else:
                c = box[r][c]
                c = str(c)
                if len(c) == 1:
                    print( "  " + c + "  ",end=' ')
                else:
                    print(' ',c,' ', end='')
        print()
#-------------------------------------------------------------------

    time.sleep(0.1)
    print("\n" * 30)

    if pathcount == len(box)*len(box[row]):
        RUN = False





row = 0
col = 0
box[row][col] = "M"
cur_path = 1
ncell = []
pathway = [] #entire pathway traveled by the mouse/pathfinder
shr_path = [] #shortest path
carved_path = [] #paths to dead ends
SEARCH = True

while SEARCH:

    i = 0
    path_retrack = False
    ncell = []
    pre_row = row #technically previous row
    pre_col = col #technically previous row

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr != 0 and dc != 0:
                continue
            elif dr == 0 and dc == 0:
                continue

            nr = row + dr
            nc = col + dc

            if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
                if cur_path - box[nr][nc] == -1: #if the diff between the current  cell and the next cell is -1,ie, going  forward
                    ncell.append([nr, nc])

    if [pre_row, pre_col]  == [len(box)-1, len(box[pre_row])-1]: #Ends path finding after reaching end
        SEARCH = False
        continue

    print("ncell : ", ncell)


    for cell_idx in range(len(ncell)): #removes already traversed paths from options so it won't follow the same dead end
        cell = ncell[cell_idx - i]
        print("cell : ", cell)
        if cell in  carved_path:
            ncell.remove(cell)
            i += 1  #to fix offset of index after removing

    print("cut ncell : ", ncell)

    if not ncell:   #if no options are available, ie, the path finding reached dead end
        path_retrack = True

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 and dc != 0:
                    continue
                elif dr == 0 and dc == 0:
                    continue

                nr = row + dr
                nc = col + dc

                if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
                    if cur_path - box[nr][nc] == 1: #if the diff between the current  cell and the next cell is 1,ie, retracking
                        ncell.append([nr, nc])

        print("new ncell : ", ncell)


    print(path_retrack)
    ocell = random.choice(ncell)
    print("ocell : ", ocell)


    row = ocell[0]
    col = ocell[1]
    cur_path = box[row][col] #the path value of current cell since it will be overwritten by "M"
    box[row][col] = "M" #retwrits current cell to "M" the mouse/pathfinder

    # assigns the value of path for the previous cell depending on if retracking or moving froward
    if path_retrack:
        box[pre_row][pre_col] = cur_path + 1
    else:
        box[pre_row][pre_col] = cur_path - 1

    pathway.insert(0,[row,col])


    if path_retrack:
        if [pre_row,pre_col] in shr_path:   #to remove the paths leading to dead ends from shortest path
            shr_path.remove([pre_row,pre_col])
            carved_path.append([pre_row,pre_col]) #adds the paths leading to dead ends to carved path
    else:
        shr_path.insert(0,[row,col])


    print("pathway : ", pathway)
    print("shr_path : ", shr_path)
    print("carved_path : ", carved_path)

#IGNORE, FOR CHECKING PATHWAY(colour and spacing based printing)----------------------
    for r in range(len(box)):
        for c in range(len(box[r])):

            if c == len(box[r])-1 and r == len(box)-1:
                x = box[r][c]
                x = str(x)
                if len(x) == 1:
                    print(" ", Fore.LIGHTGREEN_EX + x,"  ", end=' ')
                else:
                    print(' ',Fore.LIGHTGREEN_EX + x,' ', end='')

            elif box[r][c] == "M":
                print(" ", Fore.YELLOW + "M", "  ", end='')

            elif c == 0 and r == 0:
                x = box[r][c]
                print(" ", Fore.RED + str(x),"  ",end='')

            else:
                x = box[r][c]


                if len(str(x)) == 1:
                    if [r,c] in shr_path:
                         print(" " , Fore.GREEN + str(x) , " ",end=' ')
                    elif [r,c] in pathway:
                        print(" " , Fore.BLACK + str(x) , " ",end=' ')
                    else:
                        print(" ", str(x) , " ",end=' ')

                else:
                    if [r,c] in shr_path:
                         print(' ' , Fore.GREEN + str(x) , ' ',end='')
                    elif [r,c] in pathway:
                        print(' ' , Fore.BLACK + str(x) , ' ',end='')
                    else:
                        print(' ' , str(x) , ' ',end='')
#-------------------------------------------------------------------------------------

        print()
    time.sleep(1.3)
    print("\n" * 30)


