from random_username.generate import generate_username 
from nltk.tokenize import word_tokenize,sent_tokenize 
import re

# welcome User
def welcomeUser(): 
    print("\nwelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():

    maxAttempts =  3 
    attempts = 0 

    while attempts < maxAttempts:
        
         # Print message prompting user to input their name
        inputPrompt = ""
        if attempts == 0:
            inputPrompt = "\nTo begin, please enter your username:\n" 
        else :
             inputPrompt = "\nPlease try again:\n"
        usernameFrominput = input(inputPrompt)
             
        # Validate username
        if len(usernameFrominput) < 5 or not usernameFrominput.isidentifier():
            print("Your username must be at least 5 characters long, alphanumeric only (a-z/A-Z/0-9),have no spaces and cannot start with a number")
        else:
            return usernameFrominput
        
        attempts += 1 

    print("\nExhausted all " + str(maxAttempts) +  " attempts,assigning new username instead...")
    return generate_username()[0]

# Greet the user
def greetUser(name):
    print("Hello, " + name)

#Get text from file 
def getArticleText():
    f = open("files/article.txt")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\r", "")

#Extract Sentences from raw Text Body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

#Extracts  Words from list of sentences
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

# Get the key sentences based on search pattern of key words
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        # If sentence matches desired pattern , add to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

#Get the average words per sentence, excluding punctuation
def getWordsPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(" "))
    return totalWords / len(sentences)

# Filter raw tokenized words list to only include
# valid english words 
def cleanseWordList(words):
    cleanseWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for word in words:
        cleansedWord = word.replace(".","").lower()
        if (not re.search(invalidWordPattern, cleansedWord)) and len(word) > 1:
            cleanseWords.append(cleansedWord)
    return cleanseWords

# Get User Details
welcomeUser() 
username = getUsername()
greetUser(username)

# Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Get Sentence Analytics 
stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
keySentences = extractKeySentences(articleSentences,stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Get word Analytics
articleWordsCleansed = cleanseWordList(articleWords)

# Print for testing
print("GOT:")
print(articleWordsCleansed)

