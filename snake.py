import os
import keyboard
from time import sleep
import random
import platform

def clear():
		if platform.system() == "Windows":
			os.system('cls')
		else:
			os.system('clear')

def printGame():                #Converts the list elements to characters and prints them
    print(borderSymbol * (cols + 2))     #Prints the borders of the region
    for i in range(rows):
        x = ""                  #Each row is converted to a single line string
        for j in range(cols):
            x += arr[i][j]      #The element of each row is a character that appends the rows' string
        print(borderSymbol + x + borderSymbol)    #Prints each row (sublist) as a string
    print(borderSymbol * (cols + 2))     #Prints the borders of the region      


#Detects and returns the key pressed by the user
def detectKeystroke(previousKey):
    keystroke = previousKey         #If no key is pressed, the previous key is returned
    if keyboard.is_pressed(leftKey):
        keystroke = "left"
    if keyboard.is_pressed(backwardKey): 
        keystroke = "backward"
    if keyboard.is_pressed(forwardKey): 
        keystroke = "forward"
    if keyboard.is_pressed(rightKey): 
        keystroke = "right"
    return keystroke

#Checks whether the head touches the border
def outOfBorder(position):
    if position[0] < 0:
        return "true"
    if position[0] > rows - 1:
        return "true"
    if position[1] < 0:
        return "true"
    if position[1] > cols - 1:
        return "true"

#Game over screen
def gameOver():
    while(1):
        clear()
        print("GAME OVER\nPRESS Q TO EXIT")
        if keyboard.is_pressed("q"):
            exit()
        sleep(0.05)

#Random fruits generator
def genfruits():
    numberOfFruits = random.randint(1, maxFruitNumber)  #The number of fruits is random
    for _ in range(numberOfFruits):
        randomY = random.randint(0, rows - 1)           #Random position is generated for each fruit
        randomX = random.randint(0, cols - 1)
        fruitCords.append([randomY, randomX])           #Positions added in the fruitCords list

def printFruits(fruitList):
    for i in fruitList:
        arr[i[0]][i[1]] = fruitSymbol

#Deals with eaten fruits
def removeFruits(eatenFruitCords):
    global fruitsFinished
    arr[eatenFruitCords[0]][eatenFruitCords[1]] = " "   #The eaten fruit character is replaced with blank
    fruitCords.remove(eatenFruitCords)                  #Its cords are removed from the list
    if len(fruitCords) == 0:                            #If all the fruits are eaten (length of list = 0), the fruitsFinished is turned to true
        fruitsFinished = "true"

#Manages the points
def pointManagement(snakeCords):
    global points
    for i in fruitCords:
        if i[0] == snakeCords[0] and i[1] == snakeCords[1]:     #Checks if the position of the snake is the same as the position of any of the heads
            points += 1                                         #A point is added
            removeFruits(i)                                     #The eaten fruit is removed

#Manages the fruits
def fruitManagement(position):
    global fruitsFinished
    if fruitsFinished == "true":    #If all fruits are eaten, new fruits are generated
        genfruits()
        fruitsFinished = "false"    #The var is false untilall the fruits get eaten again
    pointManagement(position)       #Responsible for adding points
    printFruits(fruitCords)

def updateTail(position):
    for i in snakeTrail:                    #The old trail is removed
        arr[i[0]][i[1]] = " "
    tempPosition = []                       #Each last location of the snake is stored in the snakeTrail list, because the tail follows the head
    tempPosition.extend(position)
    snakeTrail.append(tempPosition)
    if points < len(snakeTrail):            #The size of the snakeTrail is regulated according to the tail characters needed and thus according to the points
        snakeTrail.remove(snakeTrail[0])

#The tail is printed
def printTail():
    for i in snakeTrail:                #Each sublist of the snakeTrail list is the position of every tail character
        arr[i[0]][i[1]] = tailSymbol    #Tail is printed as "*"

#Checks if tail touches the head
def headInTail(position):
    for i in snakeTrail:
        if i == position:   #Checks if the position of any of the tail characters is the same as the position of the head
            return "true"

#Responsible for the movement of the snake
def snakeMovement():                            
    position = [rows//2, cols//2]           #Sets the initial position of the snake      
    keyPressed = initialDirection           #Sets the initial direction by setting the first pressed key
    while(1):
        updateTail(position)                        #The location (before it changes to a new one) is processed and stored in this function; used to know where the tail is
        keyPressed = detectKeystroke(keyPressed)    #Detect which key is pressed
        arr[position[0]][position[1]] = " "         #The previous location of the 'X' (head) turns into blank, to give the sense of movement
        
        #The if statements change the position according to the pressed key
        if keyPressed == "forward":                       
            position[0] -= 1
        if keyPressed == "backward":
            position[0] += 1
        if keyPressed == "right":
            position[1] += 1
        if keyPressed == "left":
            position[1] -= 1
        
        #If the snake hits the border or eats its tail, the game halts
        if outOfBorder(position) == "true" or headInTail(position) == "true":
            gameOver()
        
        fruitManagement(position)                   #Anything that has to do with fruits is managed by this function
        arr[position[0]][position[1]] = headSymbol  #The head appears in the new position

        printTail()                                 #The tail is printed
        printGame()                                 #The screen is refreshed
        
        print("Points: {}".format(points))          #Display of points

        if keyPressed == "forward" or keyPressed == "backward":  #Changes the refresh rate / movement speed according to the direction of movement
            sleep(2/speed)
        else:
            sleep(1/speed)                              
        
        clear()                           #The screen is cleared

#Game settings
rows, cols = (15, 40)                       #Setting the size of the game region
speed = 40                                  #Set moving speed
borderSymbol = "#"
headSymbol = "@"
tailSymbol = "+"
fruitSymbol = "O"
maxFruitNumber = 6
forwardKey = "w"
backwardKey = "s"
leftKey = "a"
rightKey = "d"
initialDirection = "forward"                       #(leave blank for the snake to be initially stopped)

#Initializing global objects
arr = [[" "] * cols for _ in range(rows)]   #Creating an empty region as a list for the snake to move in
points = 0                                  #Initializing points
fruitCords = []                             #Variable used to store the position of fruits
fruitsFinished = "true"                     #When it is true, new fruits are generated
snakeTrail = []                             #Used to generate the tail

#Calling the main function
snakeMovement()
