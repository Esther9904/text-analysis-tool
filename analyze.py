from random_username.generate import generate_username

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

welcomeUser() 
username = getUsername()
greetUser(username)

