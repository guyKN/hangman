import sys
try:
    import random
    import shelve
    import re
    d = shelve.open("hangman.dat")
    modes = d["modes"] # The object listing the diffrent play modes and the words used in each mode
except ImportError:
    print("This program only works for python3. Please update to python3. ")
    sys.exit()
except (KeyError, FileNotFoundError) as e:
    print("The hangman shelve file was not found on your computer. Please download it from github. ")
    sys.exit()

    

maxLives = 7

def validWord(word): 
    # Given a word, return true if it only contains letters and is not blank. Otherwise return false. 
    return (not re.search("[^a-zA-Z]", word)) and (word != "")

def validLetter(letter, usedLetters):
    # Checks if the Letter entered is valid. 
    # If the input is not a single letter or contains a character other than a letter, return 0. 
    # If the input is a letter that has already been used, return 1.
    # If the input is valid, return 2. 
    
    if(re.search("[a-zA-Z]", letter) and (len(letter) == 1)): # Checks if the input is of lengh 1 and is a letter. 
        if(letter in usedLetters): # Checks if the letter has been used before
            return 1
        else:
            return 2
    else:
        return 0
        

def selectMode():
    # Takes player input on which mode the player wants
    while True:
        index = 0 # Counts how many times it went through the FOR loop, so it can update the numbers written
        print ("Modes: ")
        for mode in modes: # For each mode, this prints out the name of the made and the number asociated with it 
            print("[{}]: {}".format(index + 1 ,mode["written_name"])) 
            index+=1
        
        try: 
            playerChoice = int(input("Select the mode you wish to play: ") ) # Stores the number that the player selected as his mode
            activeMode = modes[playerChoice - 1] # Stores the mode the player chose as a mode object
            return activeMode # If the player entered something valid, stop the While loop to continue
        except (IndexError, ValueError) as e: # Run this if the player entered an invalid number or didn't enter a number at all
            print ("What you entered was invalid please enter a number from 1 to 4. ")

def printState(word, discoveredLetters, lives, usedLetters):
    # Prints the information the user needs to know
    wordToPrint = "" # The word, except with letters the use doesn't know are replaced with underscores. 
    for i in range(len(word)):
        if discoveredLetters[i]:
            wordToPrint+= word[i] + " "
        else:
            wordToPrint += "_ "
    print (wordToPrint)
    print("Lives Left: {}".format(lives))
    if usedLetters == []: # Checks if the user hasn't guessed any letters previosly, So it can print [None] instead of an empty list. 
        print("Letters you have already Guessed: [None]")
    else:
        print ("Letters you have already Guessed: " + ", ".join(usedLetters))

def updateState(word, discoveredLetters, lives, usedLetters, letter):
    # Checks if the user guessed right, then upgrades everything acordingly.  
    usedLetters.append(letter) 
    indices = [i for i, x in enumerate(word) if x == letter] # Finds every time that the letter is in the word
    for index in indices:
        discoveredLetters[index] = True 
    if indices == []: # Run this if the player didn't make any correct guesses. 
        lives -= 1
    return (discoveredLetters, lives, usedLetters)

    


def setUpGame():
    # Sets the game up by letting the user select the mode and then choosing a random word based on mode chosen. 
    #Returns the chosen word
    
    
    mode = selectMode()
    
    if mode["playerSelect"]: # Do this part if the player chose to select the word themselves
        while True: # 
            word = input("Please Choose a word: ")
            word = word.lower() # Replace all uppercase letters with lowercase letters
            if validWord(word): # Checks if the word has only letters and isn't blank
                break # The player has entered a valid word, so you may continue to the next part
            else:
                print ("The word you entered was invalid. Please make sure your word only has letters and try again.")
    else:
        word = random.sample(mode["words"], 1)[0] # Chooses a random word from the list of words, based on difficulty
        word = word.lower()
    word = list(word) # Makes the word into an list of letters. 
    return word
        
        
def playGame(word):
    # Given a specific word, play the game 
    #print (word) # For testing only
    discoveredLetters = [False]*len(word) # A list that has each element represent wether or not the specific player has discovered the letter at the given index. 
    lives = maxLives # Stores how many 
    usedLetters = []
    print ("") # Creates a line space
    while True:
        if lives == 0: # The player has ran out of lives. 
            printState(word, [True]*len(word), lives, usedLetters) # Prints the state, except that all letters are relvealed
            print("You lost. Better luck next time. The answer was \"{}\"".format("".join(word)))
            break
        if False not in discoveredLetters: # The player has guessed every letter in the word. They won
            printState(word, discoveredLetters, lives, usedLetters)
            print ("Good job. You won!")
            break
        while True: # Have player select the letter they want to guess. 
            printState(word, discoveredLetters, lives, usedLetters)
            letter = input("Guess a letter: ")
            letter = letter.lower() # Makes the letter into lowercase so it's not case sensative. 
            letterValidity = validLetter(letter, usedLetters) # Stores wether the letter is valid. 
            if (letterValidity == 0): 
                print("\nWhat you entered was invalid. Please enter a single letter. ")
            elif (letterValidity == 1): 
                print("\nYou've already guessed that letter. Please guess a letter you haven't guessed before. ")
            elif (letterValidity == 2):
                break # The letter is valid
        discoveredLetters, lives, usedLetters = updateState(word, discoveredLetters, lives, usedLetters, letter) # Updates everything
        print("") # Creates a line space
def main():    
    playAgain = True
    print("Welcome to Hangman")

    while playAgain:
        word = setUpGame()
        playGame(word)
        while True: 
            inp = input("would you like to play again?[Y/n]: ")
            inp = inp.lower() # Make sure the input is not case sensetive
            if inp == "y":
                break
            if inp == "n":
                playAgain = False
                break
                
if __name__ == '__main__':
    main()

    
