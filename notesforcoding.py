print ("hi")
print("my name is sigma")
sigma=10
print(sigma)
print(f"i love {sigma}")



#In Python, you don't need complex boilerplate code.
#  To show text on the screen, you use the print() function.
print("Hello, Python!")

#Variables are like boxes that store information. 
# You don't need to declare what "type" of data they hold;
#  Python figures it out for you.
name = "Tamilore"      # A String (text)
age = 20               # An Integer (whole number)
height = 5.9           # A Float (decimal)
is_coding = True       # A Boolean (True/False)
#Python works like a calculator.
sum = 10 + 5           # Addition
product = 10 * 5       # Multiplication
exponent = 2 ** 3      # 2 to the power of 3 (8)

#This is how your code makes decisions. 
# Note: Python uses indentation (tabs or spaces) 
# to know which code belongs inside the "if" statement.

age = 18

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")


    #Loops let you repeat actions without writing the code over and over.
for i in range(5):
    print("Loop number:", i)


#Instead of making ten variables for ten names, 
# you can use a List. Lists are ordered and changeable.
    
fruits = ["apple", "banana", "cherry"]

print(fruits[0])      # Output: apple (Python starts counting at 0!)
fruits.append("kiwi") # Adds "kiwi" to the end

#Functions are like "recipes." 
# You define them once and call them whenever you need that specific task done. 
# This keeps your code clean.


def greet_user(username):
    print("Hello, " + username + "!")

# To use it:
greet_user("Tamilore")
#Dictionaries store data in pairs. 
# Think of a real dictionary: 
# you have the word (the key) 
# and the definition (the value).

player = {
    "name": "Tamilore",
    "level": 5,
    "health": 100
}

print(player["level"]) # Output: 5


#You can make your programs interactive by asking the user for information. 
# Note that input always comes in as text (a string), 
# so if you want to do math with it, you have to convert it.

user_name=input("Enter your name")
user_age =int(input('Enter your age')) # Converts the text to a number

print(f"Next year, {user_name} will be {user_age + 1} years old.")

#The Power of f-strings: 
# Notice the f"..." in the example above? That’s called an f-string. 
# It’s the easiest way to put variables inside a sentence without messy plus signs.

#Comments are your friends:
# Use the # symbol to write notes to yourself. 
# Python ignores them,
#  but they’ll save you hours of confusion when you look at your code a week later.

#Errors are normal:
#  If you see a wall of red text (a Traceback), don't panic. 
# Read the very last line—it usually tells you exactly what went wrong 
# (e.g., NameError or SyntaxError).





#One of Python’s greatest strengths is its "batteries included" philosophy. 
# You don't have to write code for complex math, random numbers,
#  or web scraping from scratch. You just import a module.
import random
import math

# Get a random number between 1 and 10
number = random.randint(1, 10)

# Calculate a square root
print(math.sqrt(16)) # Output: 4.0

#Programs crash if the user does something unexpected 
# (like typing "abc" when you asked for a number).
#  You can "catch" these errors so your program stays running.
try:
    age = int(input("Enter your age: "))
    print(f"You are {age} years old.")
except ValueError:
    print("That wasn't a number! Please try again.")


#This is a "fancy" Python trick that makes your code much shorter. 
# It’s a way to create a new list based on an old one in just one line.
# Traditional way to square numbers:
numbers = [1, 2, 3, 4, 5]
squares = []
for n in numbers:
    squares.append(n * n)

# The Pythonic way (List Comprehension):
squares = [n * n for n in numbers]
#Coding is mostly about logic.
#  You can combine conditions using and, or, and not.
#and: Both must be true.
#or: At least one must be true.
#not: Flips the result (True becomes False).
#Python can read and write files on your computer. 
#The with keyword is the best way to do this because it closes the file automatically when you're done.
# Writing to a file
with open("notes.txt", "w") as file:
    file.write("I am learning Python!")

# Reading from a file
with open("notes.txt", "r") as file:
    content = file.read()
    print(content)
    #How to actually "Learn" coding
#The biggest mistake beginners make is watching instead of doing.

#Break things: Change a variable name or delete a colon and see what error pops up. Learning to read errors is 50% of the job.

#The 20-Minute Rule: If you get stuck on a bug, try to solve it for 20 minutes. If you still can't, Google the error message.

#Build a "Garbage" Project: Don't try to build the next Instagram yet. Build a simple "Rock, Paper, Scissors" game or a "Tip Calculator."
