# welcome User
def welcomeUser(): 
    print("\nwelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    # Print message prompting user to input their name  
    usernameFrominput = input("\nTo begin, please enter your username:\n")
    return usernameFrominput

# Greet the user
def greetUser(name):
    print("Hello, " + name)

welcomeUser() 
username = getUsername()
greetUser(username)

