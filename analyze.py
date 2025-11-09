from random_username.generate import generate_username

# welcome User
def welcomeUser(): 
    print("\nwelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    # Print message prompting user to input their name  
    usernameFrominput = input("\nTo begin, please enter your username:\n") 

    if len(usernameFrominput) < 5 or not usernameFrominput.isidentifier():
        print("Your username must be at least 5 characters long, alphanumeric only (a-z/A-Z/0-9),have no spaces and cannot start with a number")
        print("Assigning new username instead...")
        return generate_username()[0]

    return usernameFrominput
    


# Greet the user
def greetUser(name):
    print("Hello, " + name)

welcomeUser() 
username = getUsername()
greetUser(username)

