import base64
from io import BytesIO
from random_username.generate import generate_username 
import re, nltk, json
from nltk.tokenize import word_tokenize,sent_tokenize 
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
nltk.download ('stopwords')
nltk.download ('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('vader_lexicon')
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()

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

# Convert part of speech from pos_tag() function
#into wordnet compatible pos tag
posToWordnetTag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}

def treebankPosToWordnet(partOfSpeech):
    posfirstChar = partOfSpeech[0]
    if posfirstChar in posToWordnetTag:
        return posToWordnetTag[posfirstChar] 
    return wordnet.NOUN

# Convert raw list of (word, POS) tuple to a list of strings
# that only include valid english words 
def cleanseWordList(posTaggedWordTuples):
    cleanseWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleansedWord = word.replace(".","").lower()
        if (not re.search(invalidWordPattern, cleansedWord)) and len(cleansedWord) > 1 and cleansedWord not in stopWords:
            cleanseWords.append(wordLemmatizer.lemmatize(cleansedWord,treebankPosToWordnet(pos)))
    return cleanseWords

def analyzeText(textToAnalyze):
    articleSentences = tokenizeSentences(textToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    # Get Sentence Analytics 
    stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
    keySentences = extractKeySentences(articleSentences,stockSearchPattern)
    wordsPerSentence = getWordsPerSentence(articleSentences)

    # Get word Analytics
    wordsPosTagged = nltk.pos_tag(articleWords)
    articleWordsCleansed = cleanseWordList(wordsPosTagged)

    # Generate word cloud
    separator = " "
    wordCloudFilePath = "results/wordcloud.png"
    wordcloud = WordCloud(width = 1000, height = 700, \
        background_color="white", colormap="Set3", collocations=False).generate(separator.join(articleWordsCleansed))
    # wordcloud.to_file(wordCloudFilePath)
    imgIo = BytesIO()
    wordcloud.to_image().save(imgIo, format='PNG')
    imgIo.seek(0)

    # Encode the image as base64
    encodedWordCloud = base64.b64encode(imgIo.getvalue()).decode('utf-8')

    #Run Sentiment Analysis
    sentimentResult = sentimentAnalyzer.polarity_scores(textToAnalyze)

    # Collate analyses into one dictionary
    finalResult = {
        "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "sentiment": sentimentResult,
            "wordCloudFilePath": wordCloudFilePath,
            "wordCloudImage": encodedWordCloud
        },
        "metadata":{
            "sentenceAnalyzed": len(articleSentences),
            "wordsAnalyzed": len(articleWordsCleansed)

        }
    }
    return finalResult
def runAsFile():
    # Get User Details
    welcomeUser() 
    username = getUsername()
    greetUser(username)

    # Extract and Tokenize Text
    articleTextRaw = getArticleText()
    analyzeText(articleTextRaw)