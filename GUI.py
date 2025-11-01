import random
import time
import pygame
import colorama

def Draw_cell(row,col,pre_row,pre_col):

    '''pre_row = pre_pathway[path][0]
    pre_col = pre_pathway[path][1]
    row = gen_pathway[path][0]
    col = gen_pathway[path][1]'''
    window.blit(cell, (col * 30, row * 30))

    if row - pre_row == -1:
        pygame.draw.line(window, (0, 0, 0), (pre_col * 30 + 1, (pre_row * 30) - 1),
                         ((pre_col * 30) + 28, (pre_row * 30) - 1), 2)
    if row - pre_row == 1:
        pygame.draw.line(window, (0, 0, 0), (pre_col * 30 + 1, (pre_row * 30) + 29),
                         ((pre_col * 30) + 28, (pre_row * 30) + 29), 2)
    if col - pre_col == 1:
        pygame.draw.line(window, (0, 0, 0), ((pre_col * 30) + 29, pre_row * 30 + 1),
                         ((pre_col * 30) + 29, (pre_row * 30) + 28), 2)
    if col - pre_col == -1:
        pygame.draw.line(window, (0, 0, 0), ((pre_col * 30) - 1, pre_row * 30 + 1),
                         ((pre_col * 30) - 1, (pre_row * 30) + 28), 2)

    window.blit(start, (0, 0))

    pygame.draw.rect(end, (255, 255, 255), end.get_rect(), 1)
    window.blit(end, ((len(box[row]) - 1) * 30, (len(box) - 1) * 30))



colorama.init(autoreset=True)

pygame.init()

a,b = 1200,750
window = pygame.display.set_mode((a,b))
pygame.display.set_caption("MAZE GEN")

#TITLE GUI
fontTITLE = pygame.font.SysFont("Sitka", 60)
TITLE = fontTITLE.render("M A Z E", True, (255,255,255))
window.blit(TITLE, (910, 25))

fontgen = pygame.font.SysFont(None, 50)
gen_text = "GENERATING..."
generating = fontgen.render(gen_text, True, (255,255,255))
window.blit(generating, (860, 340))

#CELL GUI
cell = pygame.Surface((30,30))
pygame.draw.rect(cell, (255,255,255), cell.get_rect(), 1)
window.blit(cell, (0,0))

trk_cell = pygame.Surface((28,28))
trk_cell.fill((0, 80, 82))

#BUTTON GUI
p_button = pygame.Surface((175,75))
p_button.fill((255,0,0))
pygame.draw.rect(p_button, (255,255,255), p_button.get_rect(), 1)
p_hb = pygame.Rect(900,170,175,75)

t_button = pygame.Surface((175,75))
t_button.fill((0,0,0))
pygame.draw.rect(t_button, (200,200,200), t_button.get_rect(), 1)
t_hb = pygame.Rect(900,370,175,75)

s_button = pygame.Surface((175,75))
s_button.fill((90,90,90))
pygame.draw.rect(s_button, (255,255,255), s_button.get_rect(), 1)
s_hb = pygame.Rect(900,600,175,75)


font = pygame.font.SysFont(None, 46)

#TEXT GUI
#pause button
p_TextWindow = font.render("PAUSED", True, (255,255,255))
p_tx1 = 21
p_tx2 = 25

#track button
t_TextWindow = font.render("TRACK", True, (255,255,255))
t_tx1 = 30
t_tx2 = 2
#y - 24

#speed button
s_TextWindow = font.render("x1", True, (20,20,20))
s_tx1 = 75
s_tx2 = 55
#y - 23

#diff tickrate events
TITLE_EVENT = pygame.USEREVENT + 1
GENERATING_EVENT = pygame.USEREVENT + 2


title_count = 0
pygame.time.set_timer(TITLE_EVENT, 1000)
pygame.time.set_timer(GENERATING_EVENT, 500)
clock = pygame.time.Clock()

#THE GRID
grid_size = 25
box = [[0]*grid_size for _ in range(grid_size)]



row = 0
col = 0
path = 1  # path of maze,the actual path
pathcount = 1  # to calc number of spaces filled
gen_pathway = [] #Generation path, contains entire pathway of the maze
pre_pathway = [] #previous gen path
box[row][col] = 1
j_cr = []  # list of jumpable cells
jrow = 0 #jumped col
jcol = 0 #jumped row
directions = [(0,1),(0,-1),(1,0),(-1,0)]

start = pygame.Surface((30,30)) #start of maze
start.fill((170, 255, 130))
end = pygame.Surface((30,30)) #end of maze
end.fill((255, 130, 130))


RUN = True

while RUN:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Title animation
        if event.type == TITLE_EVENT:
            title_count += 1  # increment each tick

            # clear old title area
            window.fill((0, 0, 0), (850, 15, 500, 80))  # x, y, width, height

            if title_count % 2 == 0:
                TITLE = fontTITLE.render("M A Z E", True, (255, 255, 255))
                window.blit(TITLE, (910, 25))
            else:
                TITLE = fontTITLE.render("MAZE", True, (255, 255, 255))
                window.blit(TITLE, (920, 25))

        #"Generating.." text animation
        if event.type == GENERATING_EVENT:

            window.fill((0, 0, 0), (860, 340, 500, 80))

            if gen_text == "GENERATING...":
                gen_text = "GENERATING.."
                generating = fontgen.render("GENERATING..", True, (255, 255, 255))

            elif gen_text == "GENERATING..":
                gen_text = "GENERATING."
                generating = fontgen.render("GENERATING.", True, (255, 255, 255))

            elif gen_text == "GENERATING.":
                gen_text = "GENERATING..."
                generating = fontgen.render("GENERATING...", True, (255, 255, 255))

            window.blit(generating, (860, 340))
            pygame.display.update()



    path_jump = False
    ncell = []  # options around the cell
    pre_row = row
    pre_col = col

    # checks all options around cell whether filled or not
    for dr,dc in directions:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
            if box[nr][nc] == 0:
                ncell.append([nr, nc])

    ori_ncell = ncell


    if not ncell: #if no options are available, ie, the cell path is stuck
        path_jump = True
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
                        if box[jr][jc] == 0: # adds empty/free options to ncell and determines if stuck true or false
                            ncell.append([jr, jc])

            if ncell: #if the chosen jumpable cell has options around it to continue moving
                break


    ocell = random.choice(ncell)
    row = ocell[0]
    col = ocell[1]

    # finds jumpable cells and adds them to list j_cr
    if len(ncell) > 1:
        j = list([pre_row, pre_col])
        j_cr.insert(0, j)


    if path_jump: #if a path had jumped, it retracks the path count
        path = box[jrow][jcol]
        pre_row = jrow
        pre_col = jcol

    path += 1
    box[row][col] = path
    pathcount += 1

    gen_pathway.append([row,col])
    pre_pathway.append([pre_row,pre_col])


    window.blit(cell, (col*30, row*30))

    #Wall drawing
    Draw_cell(row, col, pre_row, pre_col)


    if pathcount == len(box)*len(box[row]):
        RUN = False

    pygame.display.update()


    clock.tick(40)


window.fill((0, 0, 0), (860, 340, 500, 80))

generating = fontgen.render("GENERATED", True, (255, 255, 255))
window.blit(generating, (860, 340))



#blinking animation after generation
for blink in range(7):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if blink %2 == 0:
        pygame.draw.rect(cell, (255,255,255), cell.get_rect(), 1)
    else:
        pygame.draw.rect(cell, (250, 230, 0), cell.get_rect(), 1)
    pygame.display.update()
    time.sleep(0.4)

    for path in range(len(gen_pathway)):
        Draw_cell(gen_pathway[path][0],gen_pathway[path][1],pre_pathway[path][0],pre_pathway[path][1])

    pygame.display.update()




window.fill((0, 0, 0), ((860, 340, 500, 80)))


row = 0
col = 0
box[row][col] = "M"
cur_path = 1
ncell = [] #neighbouring cells
pathway = [] #entire pathway traveled by the mouse/pathfinder
shr_path = [] #shortest path
carved_path = [] #paths to dead ends
mouse = pygame.Surface((20,20))
mouse.fill((255, 248, 59))

PAUSED = True
TRACKING = False
SPEED = 500
SEARCH = True
p_tx = p_tx1
t_tx = t_tx1
s_tx = s_tx1

while SEARCH:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == TITLE_EVENT:
            title_count += 1  # increment each tick

            # clear old title area
            window.fill((0, 0, 0), (850, 15, 500, 80))  # x, y, width, height

            if title_count % 2 == 0:
                TITLE = fontTITLE.render("M A Z E", True, (255, 255, 255))
                window.blit(TITLE, (910, 25))
            else:
                TITLE = fontTITLE.render("MAZE", True, (255, 255, 255))
                window.blit(TITLE, (920, 25))

        #Button press event
        if event.type == pygame.MOUSEBUTTONDOWN:
            mos_pos = event.pos

            if p_hb.collidepoint(mos_pos):
                if PAUSED:
                    PAUSED = False
                    p_button.fill((0,255,0))
                    p_TextWindow = font.render("PLAYING", True, (255, 255, 255))
                    p_tx = p_tx1

                else:
                    PAUSED = True
                    p_button.fill((255,0,0))
                    p_TextWindow = font.render("PAUSED", True, (255, 255, 255))
                    p_tx = p_tx2
                pygame.display.update()


            if t_hb.collidepoint(mos_pos):
                if TRACKING:
                    TRACKING = False
                    t_button.fill((0,0,0))
                    pygame.draw.rect(t_button, (200,200,200), t_button.get_rect(), 1)
                    t_TextWindow = font.render("TRACK", True, (255,255,255))
                    t_tx = t_tx1

                else:
                    TRACKING = True
                    t_button.fill((255,255,255))
                    t_TextWindow = font.render("TRACKING", True, (0,0,0))
                    t_tx = t_tx2
                pygame.display.update()

            if s_hb.collidepoint(mos_pos):
                if SPEED == 500:
                    SPEED = 400
                    s_TextWindow = font.render("x1.5", True, (20,20,20))
                    s_tx = s_tx2

                elif SPEED == 400:
                    SPEED = 200
                    s_TextWindow = font.render("x2", True, (20,20,20))
                    s_tx = s_tx1

                elif SPEED == 200:
                    SPEED = 50
                    s_TextWindow = font.render("x3", True, (20,20,20))
                    s_tx = s_tx1

                elif SPEED == 50:
                    SPEED = 750
                    s_TextWindow = font.render("x0.5", True, (20,20,20))
                    s_tx = s_tx2

                elif SPEED == 750:
                    SPEED = 500
                    s_TextWindow = font.render("x1", True, (20,20,20))
                    s_tx = s_tx1


    i = 0
    path_retrack = False
    ncell = []
    pre_row = row # previous row
    pre_col = col # previous col

    if not PAUSED:
        if [pre_row, pre_col]  != [len(box)-1, len(box[pre_row])-1]:
            for dr,dc in directions:
                nr = row + dr
                nc = col + dc

                if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
                    if cur_path - box[nr][nc] == -1: #if the diff between the current  cell and the next cell is -1,ie, going  forward
                        ncell.append([nr, nc])

            if [pre_row, pre_col]  == [len(box)-1, len(box[pre_row])-1]: #Ends path finding after reaching end
                SEARCH = False
                continue


            for cell_idx in range(len(ncell)): #removes already traversed paths from options so it won't follow the same dead end
                cell_opt = ncell[cell_idx - i]
                if cell_opt in  carved_path:
                    ncell.remove(cell_opt)
                    i += 1  #to fix offset of index after removing


            if not ncell:   #if no options are available, ie, the path finding reached dead end
                path_retrack = True

                for dr, dc in directions:
                    nr = row + dr
                    nc = col + dc

                    if 0 <= nr < len(box) and 0 <= nc < len(box[row]):
                        if cur_path - box[nr][nc] == 1: #if the diff between the current  cell and the next cell is 1,ie, retracking
                            ncell.append([nr, nc])


            ocell = random.choice(ncell)


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



        else:
            pygame.draw.rect(cell, (255,255,0), cell.get_rect(), 1)


    #Refreshes the screen each tick
    for path in range(len(gen_pathway)):
        Draw_cell(gen_pathway[path][0],gen_pathway[path][1],pre_pathway[path][0],pre_pathway[path][1])


    if TRACKING:
        for track_cell in shr_path:
            trow = track_cell[0]
            tcol = track_cell[1]

            window.blit(trk_cell, (tcol*30+1, trow*30+1))



    window.blit(p_button,  (900,170))
    pygame.draw.rect(p_button, (255, 255, 255), p_button.get_rect(), 1)
    window.blit(p_TextWindow, (900+p_tx ,193))

    window.blit(t_button, (900,370))
    pygame.draw.rect(t_button, (255, 255, 255), t_button.get_rect(), 1)
    window.blit(t_TextWindow, (900+t_tx ,393))

    window.blit(s_button, (900,600))
    pygame.draw.rect(s_button, (255, 255, 255), s_button.get_rect(), 1)
    window.blit(s_TextWindow, (900+s_tx, 623))


    window.blit(mouse, ((col*30)+5,(row*30)+5))
    pygame.display.update()

    window.fill((0, 0, 0), (0,0,750,750))
    clock.tick(60)
    pygame.time.wait(SPEED)


#SCREEN AFTER SOLVING IS COMPLETE
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    pygame.draw.rect(cell, (255, 255,0), cell.get_rect(), 1)

    for path in range(len(gen_pathway)):
        Draw_cell(gen_pathway[path][0],gen_pathway[path][1],pre_pathway[path][0],pre_pathway[path][1])

    pygame.display.update()