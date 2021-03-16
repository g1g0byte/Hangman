import random
import os
def clear():
	os.system('cls' if os.name=='nt' else 'clear')

pics = ["  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========", 

        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",

        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",

        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========", 

        "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",

        "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",

        "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n=========",

		"  O   \n \|/  \n / \   \n"] 

def ReadFile():
	word_list=[]
	with open('words.txt','r') as file:
		for line in file:
			word_list.append(line.rstrip()) #rstrip() removes backspaces at end of .txt lines
	return word_list

def gameLoop():
	#Select random word from word list
	chosenWord = ChooseWord(word_list)
	
	#Get the ASCII values of each letter in the word
	asciiValues = GetWordASCIIValues(chosenWord)

	#Get amount of unique letters in the word
	uniqueLettersAmount, uniqueLetters = GetAmountOfUniqueLetters(chosenWord)

	#Create array containing guessed letters of the word for the player
	playersVisibleWord = CreatePlayersVisibleWordArray(chosenWord)

	print("\n")

	#Loop through the game until they lose (run out of attemptsRemaining) or win
	currentPicIndex = 0
	correctGuesses = 0
	attemptsRemaining = 6
	previousGuesses = []
	isCorrectChr = bool
	
	while attemptsRemaining > 0:
		#Print picture and visible word to player
		print(pics[currentPicIndex])
		PrintPlayersVisibleWord(playersVisibleWord)

		# Get players selected letter
		chosen_chr = PlayerInput()
		
		#Check if guessed letter has already been guessed
		alreadyGuessedMessage = "You have already selected this letter!\n"
		while chosen_chr in previousGuesses:
			print(alreadyGuessedMessage)
			chosen_chr = PlayerInput()
		previousGuesses.append(chosen_chr)

		#Check if players letter is correct or not
		isCorrectChr = CheckChosenChr(chosen_chr, asciiValues, isCorrectChr)

		#Reduce attemptsRemaining & change picture if failed to guess a correct letter
		if isCorrectChr == False:
			attemptsRemaining -= 1
			currentPicIndex += 1

		#If correct letter is guessed then make letters visible on word and add to correct guesses
		else:
			EditPlayersVisibleWord(playersVisibleWord, asciiValues, chosen_chr)
			correctGuesses += 1
	
		#Check if player has guessed all letters
		if correctGuesses == uniqueLettersAmount:
			finishedGame(True,chosenWord,playersVisibleWord,currentPicIndex,asciiValues,uniqueLetters,uniqueLettersAmount)
			return
		#Check if player has run out of attempts
		elif attemptsRemaining <= 0:
			finishedGame(False,chosenWord,playersVisibleWord,currentPicIndex,asciiValues,uniqueLetters,uniqueLettersAmount)
			return

		print("Correct guesses:", correctGuesses)
		print("attempts remaining:", attemptsRemaining)
		print("\n")

def ChooseWord(word_list):
  amountOfWords = len(word_list)
  RandomIndex = random.randint(0,amountOfWords-1)
  chosenWord = word_list[RandomIndex]

  return chosenWord

def GetWordASCIIValues(chosenWord):
  	asciiValues = []
  	for i in range(len(chosenWord)):
		  asciiValues.append(ord(chosenWord[i]))

  	return asciiValues

def GetAmountOfUniqueLetters(chosenWord):
	uniqueLetters = []
	uniqueLetters.append(chosenWord[0])
	for i in range(1,len(chosenWord)):
		if chosenWord[i] not in uniqueLetters:
			uniqueLetters.append(chosenWord[i])
	uniqueLettersAmount = len(uniqueLetters)
	
	return uniqueLettersAmount, uniqueLetters

def CreatePlayersVisibleWordArray(chosenWord):
	playersVisibleWord = []
	for i in range(len(chosenWord)):
		  playersVisibleWord.append("_")

	return playersVisibleWord

def PlayerInput():
	inputMessage = "Enter a letter: "
	errorMessage = "Please enter a single enlgish letter!"

	playerInput = input(inputMessage)

	while playerInput.isalpha() == False or len(playerInput) > 1:
		print(errorMessage)
		playerInput = input(inputMessage)

	return playerInput

def CheckChosenChr(chosen_chr, asciiValues, isCorrectChr):
	if ord(chosen_chr) not in asciiValues:
		# print("Incorrect letter, you suck")
		isCorrectChr = False
	else:
		# print("Correct letter, wow")
		isCorrectChr = True

	return isCorrectChr

def EditPlayersVisibleWord(playersVisibleWord, asciiValues, chosen_chr):
	for i in range(len(asciiValues)):
		if ord(chosen_chr) == asciiValues[i]:
			playersVisibleWord.pop(i)
			playersVisibleWord.insert(i, chosen_chr)
		
	return playersVisibleWord

def PrintPlayersVisibleWord(playersVisibleWord):
	for i in range(len(playersVisibleWord)):
		print(playersVisibleWord[i], end = " ")
	print()

def finishedGame(playerWon,chosenWord,playersVisibleWord,currentPicIndex,asciiValues,uniqueLetters,uniqueLettersAmount):
	winMessage = "You win!"
	loseMessage = "You lose!"
	wordWasMessage = "The word was: " + chosenWord

	if playerWon == True:
		print(pics[7])
		PrintPlayersVisibleWord(playersVisibleWord)
		print(winMessage, wordWasMessage)
	else:
		print(pics[currentPicIndex])
		PrintPlayersVisibleWord(playersVisibleWord)
		print(loseMessage, wordWasMessage)
	PrintInfo(chosenWord, asciiValues, uniqueLetters, uniqueLettersAmount)
	PlayAgain()

def PlayAgain():
	inputMessage = "Do you wish to play again? (y or n): "
	errorMessage = "Please enter a valid yes or no answer!"
	validYesAnswers = ["Y","y","Yes","yes"]
	validNoAnswers = ["N","n","No","no"]

	playerInput = input(inputMessage)

	while playerInput not in validYesAnswers and playerInput not in validNoAnswers:
		print(errorMessage)
		playerInput = input(inputMessage)
	
	if playerInput in validYesAnswers:
		clear()
		gameLoop()
		return
	else:
		quit()

def PrintInfo(chosenWord, asciiValues, uniqueLetters, uniqueLettersAmount):
	print("\nChosen word:", chosenWord)
	print("ASCII values of word letters array:", asciiValues)
	print("Unique letters array:", uniqueLetters)
	print("Amount of unique letters in word:", uniqueLettersAmount, "\n")
	

#Main Program
word_list = ReadFile()
gameLoop()
