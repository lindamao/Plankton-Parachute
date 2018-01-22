#####################################################################
#                           PLANKTON PARACHUTE                      #
#                    ==============================                 #
#                           NAME: LINDA MAO                         #
#                           COURSE: ICS 3UI                         #
#                        TEACHER: MR. SCHATTMAN                     #
#####################################################################

from tkinter import *
from random import*
from time import*

#Tkiner Setup
root = Tk()
root.title("Plankton Parachute")
screen = Canvas(root, width = 600, height = 700, background = "white")
screen.pack()

#Sets global initial values
def setInitialValues():
    
    global planktonX, planktonY, plankton
    global wordList, words, numberList1, numberList2, sumNumberList, numbers
    global speed, wordGenerateSpeed, mathGenerateSpeed
    global lives, score
    global userWord, userNumber
    global printInput, printScore, printLife, backToMenu
    global lineY

    #Plankton Arrays
    planktonX = []
    planktonY = []
    plankton = []

    #Word Arrays
    wordList = []
    words = []

    #Math Arrays
    numberList1 = []
    numberList2 = []
    sumNumberList = []
    numbers = []
    
    #Initial Speed Values
    speed = 3
    wordGenerateSpeed = 30
    mathGenerateSpeed = 50

    #General starting statistic values
    lives = 8
    score = 0

    #User inputs
    userWord = ""
    userNumber = ""

    #Print statistics
    printInput = None
    printScore = None
    printLife = None
    backToMenu = False

    #Line
    lineY = 540

#Draws the background        
def drawBackground():
    global scenery, sceneryImage, castle, castleImage, wall, wallImage, planktonSuccess
    
    #Draws background scenery
    scenery = PhotoImage (file="background.gif")
    sceneryImage = screen.create_image(300, 350, image = scenery)

    #Draws Krusty Krab
    castle = PhotoImage (file="krusty-krab.gif")
    castleImage = screen.create_image(310, 560, image = castle)

    #Draws Scoreboard
    screen.create_text(475, 20, text = "SCORE", font="Helvetica 10", fill="white")
    screen.create_rectangle(450, 30, 580, 60, fill = "orange2", outline = "orange2")

    #Draws Life counter
    screen.create_text(470, 70, text = "LIVES", font="Helvetica 10", fill="white")
    screen.create_rectangle(450, 80, 580, 110, fill = "sienna1", outline = "sienna1")

    #Draws input bar
    screen.create_rectangle(20, 640, 170, 670, fill = "thistle", outline = "thistle")

    #Draw line
    screen.create_line(0, lineY, 50, lineY, fill = "white")
    screen.create_line(550, lineY, 600, lineY, fill = "white")

#Draw menu button
def menuButton():
    global menuX, menuY, home, homeButton, menuW
    
    menuX = 550
    menuY = 650
    menuW = 55

    home = PhotoImage (file = "homeButton.gif")

    homeButton = screen.create_image(menuX, menuY, image = home)
    
#Checks if user clicked the menu button
def clickMenu(event):
    global backToMenu
    
    xMouse = event.x
    yMouse = event.y

    #Goes back to menu if the user click is near button
    if xMouse >= menuX - menuW/2 and xMouse <= menuX + menuW/2 and yMouse >= menuY - menuW/2 and yMouse <= menuY + menuW/2:
        menu()
        backToMenu = True

#Ending screen
def endingScreen():
    global menuScenery, menuSceneryImage
    
    menuScenery = PhotoImage (file="gameOver.gif")
    menuSceneryImage = screen.create_image(300, 350, image = menuScenery)

    menuButton()
    
#Display score statistics
def scoreStats():
    global printScore

    screen.delete(printScore)
    printScore = screen.create_text(500, 45, text = score, font = "Helvetica 15", fill = "white")

#Display life statistics
def lifeStats():
    global printLife

    screen.delete(printLife)
    printLife = screen.create_text(500, 95, text = lives, font = "Helvetica 15", fill = "white")

#Exit program through ESC key
def close(event):
    root.destroy
    exit()
    
#=============================================================================#
#                               TYPING GAME                                   #
#=============================================================================#

#Choose words
def chooseWord():
    word = choice(open("Words.txt").readlines()).replace("\n", "")
    return word

#Add values for word and Plankton
def generateWord():
    global planktonImage
    
    planktonImage = PhotoImage (file="plankton.gif")

    x = randint(50, 550)
    y = 0
    
    choose = chooseWord()
    wordList.append(choose)

    #Generate a plankton/word
    p = screen.create_image(x, y, image = planktonImage)
    word = screen.create_text(x, y, text = choose, font = "Helvetica 15", fill = "white")

    screen.delete(word, p)
    
    planktonX.append(x)
    planktonY.append(y)

    plankton.append(p)
    words.append(word)
                
#Drops plankton and words down from screen
def drop(i):
    planktonY[i] = planktonY[i] + speed

    plankton[i] = screen.create_image(planktonX[i], planktonY[i], image = planktonImage)
    words[i] = screen.create_text(planktonX[i], planktonY[i] - 50, text = wordList[i], font = "Helvetica 15", fill = "white")

#Determines whether or not user input matches any of the words on screen
def checkUserInput(u, w):
    global score, lives

    #Returns True if the input matches
    if u == w:
        i = wordList.index(w)
        screen.delete(plankton[i], words[i])
        score = score + 100

        del planktonX[i], planktonY[i], wordList[i], words[i], plankton[i]
        return True

    #Returns False if the input doesn't match
    else:
        return False

#User word input
def userInput(event):
    global userWord, printInput, lives, score, wordList, printLetter, minusLife, backToMenu

    #Array of all letters of alphabet  
    letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    alphabet = event.keysym

    #Adds each keyboard input to the total user input
    if alphabet in letter:
        userWord = userWord + alphabet

    #Delete a character if Backspace is pressed   
    elif alphabet == "BackSpace":
        userWord = userWord[0:-1]

    #Checks if user input matches word when user hits Return 
    elif alphabet == "Return":
        skip = False
        
        for word in wordList:
            check = checkUserInput(userWord, word)

            #Break the loop if the input does match
            if check == True:
                break

            #Takes away a life if it does not match
            elif check == False and skip == False:
                lives = lives - 1
                i = wordList.index(word)
                minusLife = screen.create_text(planktonX[i] + 50, planktonY[i], text = "lives -1", font = "Helvetica 12", fill = "white")
                skip = True

        userWord = ""
        
    screen.delete(printInput)
    printInput = screen.create_text(100, 658, text = userWord, font="Helvetica 18", fill="#121212")     

#=============================================================================
    
#Runs the main word game function        
def runWordGame():
    global wordGenerateSpeed, lives
        
    setInitialValues()    
    drawBackground()
    menuButton()

    #Counts each frame                  
    f = -1

    #Runs through loop as long as user still has lives
    #Also makes sure loop doesn't run when back in menu
    while lives > 0 and backToMenu == False:

        f = f + 1

        #Increase generation speed
        if f % 30 == 0:
            if wordGenerateSpeed > 10:
                wordGenerateSpeed = wordGenerateSpeed - 1

        #Generates a new word based on generation speed        
        if f % wordGenerateSpeed == 0:
            generateWord()
            
        for i in range (len(plankton)):
            drop(i)
            
        scoreStats()
        lifeStats()

        screen.update()
        sleep(0.05)

        for i in range (len(plankton)):
            screen.delete(plankton[i], words[i])

        #Checks and takes life off words that are missed
        try:
            for i in range (len(plankton)):
                
                if planktonY[i] + 50 > lineY:
                    screen.delete(plankton[i], words[i])
                    lives = lives - 1

                    minusLife = screen.create_text(planktonX[i] + 50, planktonY[i], text = "lives -1", font = "Helvetica 12", fill = "white")
                    del planktonX[i], planktonY[i], wordList[i], words[i], plankton[i]

        except:
            pass

        screen.bind("<Key>", userInput)
        screen.bind("<Button-1>", clickMenu)
        screen.bind("<Escape>", close)

        screen.focus_set()

    if backToMenu == False:
        endingScreen()

    else:
        menu()
        
#============================================================================#
#                                ADDITION GAME                               #
#============================================================================#

#Choose number 1
def chooseNumber1():
    number1 = randint(0,10)
    return number1

#Choose number 2
def chooseNumber2():
    number2 = randint(0,100)
    return number2

#Get the sum of number 1 and number 2
def getSum(a, b):
    numberSum = a + b
    return numberSum

#Add values for numbers and Plankton
def generateNumber():
    global planktonImage
    
    planktonImage = PhotoImage (file="plankton.gif")

    x = randint(50, 550)
    y = 0

    choose1 = chooseNumber1()
    numberList1.append(choose1)
    
    choose2 = chooseNumber2()
    numberList2.append(choose2)

    sumNumber = getSum(choose1, choose2)
    sumNumberList.append(sumNumber)

    #Generate a plankton/number
    p = screen.create_image(x, y, image = planktonImage)
    number = screen.create_text(x, y, text = str(choose1) + " + " + str(choose2), font = "Helvetica 15", fill = "white")

    screen.delete(p, number)
    
    planktonX.append(x)
    planktonY.append(y)

    numbers.append(number)
    plankton.append(p)

#Drops plankton and numbers down from screen
def dropNumber(i):
    planktonY[i] = planktonY[i] + speed

    plankton[i] = screen.create_image(planktonX[i], planktonY[i], image = planktonImage)
    numbers[i] = screen.create_text(planktonX[i], planktonY[i] - 50, text = str(numberList1[i]) + " + " + str(numberList2[i]), font = "Helvetica 15", fill = "white")

#Determines whether or not user input matches any of the sums on screen
def checkUserInputNumber(u, s):
    global score, lives

    #Returns True if the input matches
    if u == s:
        i = sumNumberList.index(s)
        screen.delete(plankton[i], numbers[i])
        score = score + 100
        
        del planktonX[i], planktonY[i], sumNumberList[i], numberList1[i], numberList2[i], numbers[i], plankton[i]
        return True

    #Returns False if the input doesn't match
    else:
        return False

#User math input
def userInputNumber(event):
    global userNumber, printInput, lives, score, numberList

    #Array of all digits
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    key = event.keysym

    #Adds each keyboard input to the total user input
    if key in number:
        userNumber = userNumber + key

    #Delete a character if Backspace is pressed      
    if key == "BackSpace":
        userNumber = userNumber[0:-1]

    #Checks if user input matches sum when user hits Return 
    elif key == "Return":
        skip = False
        
        for sumNumber in sumNumberList:
            check = checkUserInputNumber(int(userNumber), int(sumNumber))

            #Break the loop if the input does match            
            if check == True:
                break

            #Takes away a life if it does not match
            elif check == False and skip == False:
                i = sumNumberList.index(sumNumber)
                minusLife = screen.create_text(planktonX[i] + 50, planktonY[i], text = "lives -1", font = "Helvetica 12", fill = "white")
                lives = lives - 1
                skip = True

        userNumber = ""
        
    screen.delete(printInput)
    printInput = screen.create_text(100, 658, text = userNumber, font="Helvetica 18", fill="#121212")     
    
#===========================================================================

#Runs main math game function        
def runMathGame():
    global mathGenerateSpeed, lives
    
    setInitialValues()
    drawBackground()
    menuButton()

    #Counts each frame                  
    f = -1

    #Runs through loop as long as user still has lives
    #Also makes sure loop doesn't run when back in menu
    while lives > 0 and backToMenu == False:

        f = f + 1

        #Increase generation speed
        if f % 50 == 0:
            if mathGenerateSpeed > 15:
                mathGenerateSpeed = mathGenerateSpeed - 1

        #Generates a new word based on generation speed
        if f % mathGenerateSpeed == 0:
            generateNumber()
            
        for i in range (len(plankton)):
            dropNumber(i)

        scoreStats()
        lifeStats()

        screen.update()
        sleep(0.05)

        for i in range (len(plankton)):
            screen.delete(plankton[i], numbers[i])

        #Checks and takes life off words that are missed
        try:
            for i in range (len(plankton)):
                
                if planktonY[i] + 50 > lineY:
                    screen.delete(plankton[i], numbers[i])
                    lives = lives - 1

                    minusLife = screen.create_text(planktonX[i] + 50, planktonY[i], text = "lives -1", font = "Helvetica 12", fill = "white")
                    del planktonX[i], planktonY[i], sumNumberList[i], numberList1[i], numberList2[i], numbers[i], plankton[i]

        except:
            pass

        screen.bind("<Key>", userInputNumber)
        screen.bind("<Button-1>", clickMenu)
        screen.bind("<Escape>", close)

        screen.focus_set()

    if backToMenu == False:
        endingScreen()

    else:
        menu()
        
#============================================================================#
#                                  MENU                                      #
#============================================================================#

#Import Menu Background Image
def menuBackground():
    global menuScenery, menuSceneryImage
    
    #Draws background scenery
    menuScenery = PhotoImage (file="menu.gif")
    menuSceneryImage = screen.create_image(300, 350, image = menuScenery)

#Set intial global button values
def initialButtonValues():
    global userX, userY, button1X, button2X, buttonY, buttonWidth
    
    userX = 300
    userY = 350

    button1X = 145
    button2X = 255

    buttonY = 250
    buttonWidth = 80

#If button #1 (word game) is pressed
def clickButton1():

    if userX >= button1X - buttonWidth and userX <= button1X + buttonWidth and userY >= buttonY - buttonWidth and  userY <= buttonY + buttonWidth:
        return True
    else:
        return False

#If button #2 (math game) is pressed
def clickButton2():
    if userX >= button2X - buttonWidth and userX <= button2X + buttonWidth and userY >= buttonY - buttonWidth and  userY <= buttonY + buttonWidth:
        return True
    else:
        return False

#Checks for the user click input    
def buttonClick(event):
    global userX, userY, wordGame, mathGame
    
    userX = event.x
    userY = event.y

    #Runs the word game function if button 1 is pressed
    if clickButton1() == True:
        runWordGame()

    #Runs the math game function if button 1 is pressed
    elif clickButton2() == True:
        mathGame = runMathGame()

#Main menu       
def menu():
    menuBackground()
    initialButtonValues()
    
    screen.bind("<Button-1>", buttonClick)

#Runs the main menu                
menu()
