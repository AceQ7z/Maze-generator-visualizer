# 🐭 Maze Visualizer
A Python maze generator and solver using pygame, with real-time animation and controls.

## Features
- Recursive backtracking maze generation  
- DFS solving animation  
- Adjustable speed and pause/resume  
- Visualized shortest path
- 25x25 grid


## IMP NOTE!! :
- This is one of my FIRST "big" projects, so i gotta say this code isnt much optimised ;-;.
- **The Gui is fixed at resolution 1200x750 and thus the window may clip out of screen for smaller resolution, so i advise changing the resolution of your screen to any adequatue size.**


## Instructions :
- There really is nothing tbh, the actaull code is the "GUI.py" which comes with buttons and stuff for more control on what you are seeing.
- There is also a console based (text-based) version for those who cant run the GUI.py because of the resolution(which i am sorry for again ;-;) or just wanna check it out. its a smaller 7x7 grid version of the maze. Warning tho, this ones even more un optimised 😅).


## Explaination :
- Generation Mechanics
  Okay i suck at explaining but i will give you what i know, how this maze generation works is that by taking a an empty grid of 25x25, each loop the "gen"(the cell that generates the maze in the begining) moves a step either up, down, left or right. while doing this it marks the path it travels as 0,1,2,3.... and so on. How it decides this is, first every cell in the grid in the begining is labbeled 0. when the cell checks for which neighbouring cell to go to, it checks if that cell has the value 0, if it does it has not been visited and is a available option for travel, if it doesnt and has some other number, it has already been visited and doesnt include that cell. During this checking(we will name this checking system "check1"), it adds the avaible options for travel(the row and coloumn of the available cell in format [row,col]) to a list called *ncell*, which refreshes every loop. the next cell will be choosen from this list
  
- Wall drawing Mechanics
  we can use the path labbeling system for drawing the walls later on, because for example, lets  take a cell somewhere in the maze. Say that the gen has travelled from the left to reach the cell, and travelled to the right of the cell. we will have something like   :  | A | B | C |  where "B" is the "cell" we are talking about. we know that the path is from left to right of the cell. how would we know where to draw the walls? its simple, if B has the path value x, A will have x-1 and C will have x + 1   :   | x-1 | x | x+1 | . Thus we can draw a wall for sides around the cell where , **current cell path - neighbouring cell path is not equal to |1| or modulus of 1**.

- Dead end while generation
  A point will come where the generation hits a dead end. For that, i have made it so that, whenever the gen goes to a new cell, it checks if the path value of the surrounding cells of that cell are 0, if more than 1 is free(ie, path value 0), it adds the row and coloumn of  the cell as a list ei, [row,col], it has walked to, to a variable called *j_cr*. This list(j_cr) contains  all the points at which the cell had more than 1 option to turn to while generating. when the cell reaches a dead end. it looks goes through *j_cr* one by one and checks if the cell at the specific row and coloumn still has free spot around it now. if it does, it jumps to that cell. when the next itteration of the loop happens, it starts from where it had jumped. and an important thing is that, upon jumping, it starts naming the path of the next cell from where the path value of the cell it had jumped to had stoped. So if it reaches a dead end and the cell is labbeled a path value 54, and jumps to a cell with path value 39, theee next cell it goes to will have paath value 40. This is neccasarry so that when generating thee walls, it doesnt draw walls between the paths.

-  Solving
  here, i am gonna be refering to the thing that solves the maze as "mouse". the mouse spawns in  at the start, row0 & col0. it doesnt really spawn in, more like renaming the current cell of concentration as "mouse". it traverses through the maze using the logic i mentioned earlier for drawing the walls but just a bit modified, if **current cell path - neighbouring cell path is equal to 1** , it goes to that cell, meanign it will only go forward, not back track, for now atleast.

- Dead end / Back tracking
  when the mouse reaches a dead end, the ncell will be empty, naturaly. Thus when this happens, when the *ncell* is empty ie, an if statement fires which does the oposite of wat the first check1 does, ie, **current cell path - neighbouring cell path is equal to -1** , it adds the previous step it has taken to *ncell*, and thus upon selection, the mouse travels backwards, retracks. This will take placee again and again, ei, the *ncell* will return empty in the check1 as it also checks for another factor before adding the option to the *ncell*, it checks if the cell it might travel to is already in a list called *pathway* which basically contains all the cell it had travelled to before. so during check1, even after back tracking once, it will still elimate the cell infront of mouse as an option from *ncell* so it doesnt keeep goign back and forth. this back tracking tackes place till the mouse reaches a cell where another option is availabe, ie, a turn it hadn't took. in this case, the *ncell* will have the value of the cell it hadnt took, so the if statement for back trakin wont fire.
