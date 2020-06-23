import os
import keyboard
from time import sleep
import random
import platform

def clear():					#Used to clear the existing text, needed for screen refreshing
	if platform.system() == "Windows":	#Runs 'clear' or 'cls', according to the operating system
		os.system('cls')
	else:
		os.system('clear')

def printGame():                		#Converts the list elements to characters and prints them
    print(borderSymbol * (cols + 2))    	#Prints the borders of the region
    for i in range(rows):
        x = ""                  		#Each row is converted to a single line string
        for j in range(cols):
            x += arr[i][j]      		#The element of each row is a character that appends the rows' string
        print(borderSymbol + x + borderSymbol)	#Prints each row (sublist) as a string
    print(borderSymbol * (cols + 2))     	#Prints the borders of the region      

def detectKeystroke(previousKey):		#Detects and returns the key pressed by the user
    keystroke = previousKey         		#If no key is pressed, the previous key is returned
    if keyboard.is_pressed(leftKey):
        keystroke = "left"
    if keyboard.is_pressed(backwardKey): 
        keystroke = "backward"
    if keyboard.is_pressed(forwardKey): 
        keystroke = "forward"
    if keyboard.is_pressed(rightKey): 
        keystroke = "right"
    return keystroke

def outOfBorder(position):			#Checks whether the head touches the border
    if position[0] < 0:				#Test for vertical axis - upper border
        return "true"
    if position[0] > rows - 1:			#Test for vertical axis - lower border
        return "true"
    if position[1] < 0:				#Test for horizontal axis - left border
        return "true"
    if position[1] > cols - 1:			#Test for horizontal axis - right border
        return "true"

def gameOver():					#Game over screen
    while(1):
        clear()
        print("GAME OVER\nPRESS Q TO EXIT")
        if keyboard.is_pressed("q"):		#Halts the execution if key 'q' is pressed
            exit()
        sleep(0.05)

def genfruits():					#Generates random coordinates for fruits
    numberOfFruits = random.randint(1, maxFruitNumber)  #The number of fruits is random - upper limit is maxFruitNumber
    for _ in range(numberOfFruits):			#Loop runs as many times as the number of fruits to generate coordinates for all the fruits
        randomY = random.randint(0, rows - 1)           #Random position is generated for each fruit in each axis
        randomX = random.randint(0, cols - 1)
        fruitCords.append([randomY, randomX])           #Positions added in the fruitCords list

def printFruits(fruitList):				#Set the fruit characters on the game screen
    for i in fruitList:
        arr[i[0]][i[1]] = fruitSymbol			#In the game board list, the elements with cords equal to those of each fruit are replaced with a symbol

def removeFruits(eatenFruitCords):			#Removes the symbol of an eaten fruit
    global fruitsFinished
    arr[eatenFruitCords[0]][eatenFruitCords[1]] = " "   #The eaten fruit character is replaced with blank
    fruitCords.remove(eatenFruitCords)                  #Its cords are removed from the list
    if len(fruitCords) == 0:                            #If all the fruits are eaten (length of list = 0), the fruitsFinished is turned to true
        fruitsFinished = "true"

def pointManagement(snakeCords):				#Point management system
    global points
    for i in fruitCords:
        if i[0] == snakeCords[0] and i[1] == snakeCords[1]:     #Checks if the position of the snake is the same as the position of any of the fruits
            points += 1                                         #A point is added
            removeFruits(i)                                     #The eaten fruit is removed

def fruitManagement(position):					#Calls all fruit-related functions
    global fruitsFinished
    if fruitsFinished == "true":    				#If all fruits are eaten, new fruits are generated
        genfruits()
        fruitsFinished = "false"    				#The variable is false until all the fruits get eaten again
    pointManagement(position)
    printFruits(fruitCords)

def updateTail(position):
    for i in snakeTrail:                    			#The old trail is removed - its characters are replaced with blank in the game screen list
        arr[i[0]][i[1]] = " "
    tempPosition = []                       			#Each last location of the snake is stored in the snakeTrail list, because the tail follows the head
    tempPosition.extend(position)
    snakeTrail.append(tempPosition)
    if points < len(snakeTrail):            			#The size of the snakeTrail is regulated according to the tail characters needed and thus according to the points
        snakeTrail.remove(snakeTrail[0])

def printTail():						#The tail is printed
    for i in snakeTrail:                			#Each sublist of the snakeTrail list is the position of every tail character
        arr[i[0]][i[1]] = tailSymbol

def headInTail(position):					#Checks if tail touches the head
    for i in snakeTrail:
        if i == position:					#Checks if the position of any of the tail characters is the same as the position of the head
            return "true"

def snakeMovement():						#Responsible for the movement of the snake
    position = [rows//2, cols//2]           	    		#Sets the initial position of the snake - middle of the game board
    keyPressed = initialDirection		    		#Sets the initial direction by setting the first pressed key
    while(1):
        updateTail(position)                        		#The location (before it changes to a new one) is processed and stored in this function; used to know where the tail is
        keyPressed = detectKeystroke(keyPressed)		#Detect which key is pressed
        arr[position[0]][position[1]] = " "         		#The previous location of the 'X' (head) turns into blank, to give the sense of movement
	
        if keyPressed == "forward":      			#The if statements change the position according to the pressed key                 
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
        
        fruitManagement(position)                   		#Anything that has to do with fruits is managed by this function
        arr[position[0]][position[1]] = headSymbol  		#The head appears in the new position

        printTail()                                 		#The tail is printed
        printGame()                                 		#The screen is refreshed
        
        print("Points: {}".format(points))          		#Display of points

        if keyPressed == "forward" or keyPressed == "backward": #Changes the refresh rate / movement speed according to the direction of movement
            sleep(2/speed)
        else:
            sleep(1/speed)                              
        
        clear()                           			#The screen is cleared


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
initialDirection = "forward"                #(leave blank for the snake to be initially stopped)

#Initializing global objects
arr = [[" "] * cols for _ in range(rows)]   #Creating an empty region as a list for the snake to move in
points = 0                                  #Initializing points
fruitCords = []                             #Variable used to store the position of fruits
fruitsFinished = "true"                     #When it is true, new fruits are generated
snakeTrail = []                             #Used to generate the tail

snakeMovement()				    #Calling the main function
