# "Guess the number" mini-project

# Author: Qisong Wang
# Last edit: 2015/09/19

# General rule: The first player (Computer) thinks of a secret 
# number in some known range while the second player (You) 
# attempts to guess the number. After each guess, the first 
# player answers either “Higher”, “Lower” or “Correct!” 
# depending on whether the secret number is higher, lower 
# or equal to the guess.


# Libraries
import simplegui
import random
import math


# Global variables
secret_number = 0
range_high = 100
range_low = 0
allowed_attempts = 7
attempts_count = 0


# Helper functions
def new_game():
    """ helper function to start and restart the game. """
    global secret_number
    global allowed_attempts
    global attempts_count
    
    # generate a secret number according to the desired range
    secret_number = random.randrange(range_low, range_high)
    # CHEATING: FOR DEBUGGING PURPOSE ONLY :)    
    # print "Secret Number: ", secret_number
    
    # Calculate the number of allowed attempts
    allowed_attempts = int(math.ceil(math.log((range_high-range_low), 2)))
    
    # Initialise the attempts count for each new game
    attempts_count = 0
    
    # Display new game range and the number of remaining attempts
    remaining_attempts = allowed_attempts - attempts_count
    print "New game. Range is ["+str(range_low)+","+str(range_high)+")"
    print "Number of remaining guesses is", remaining_attempts 
    print


# Event handlers
def range100():
    """ button that changes the range to [0,100) and starts a new game """ 
    global range_high
    range_high = 100
    new_game()


def range1000():
    """ button that changes the range to [0,1000) and starts a new game """     
    global range_high
    range_high = 1000
    new_game()
    
def input_guess(guess):
    """ input field handler that deal with main game logic """
    global attempts_count
    
    # Display current guess and number of remaining attempts
    print "Guess was " + guess
    attempts_count += 1 
    remaining_attempts = allowed_attempts - attempts_count
    print "Number of remaining guesses is", remaining_attempts
    
    # Convert guess into integer so that it can be compared
    # with the secret number, and give the result according
    # to the rule shown at the top
    guess_int = int(guess)

    if remaining_attempts > 0:
        if guess_int < secret_number:
            guess_result = "Higher!"
        elif guess_int > secret_number:
            guess_result = "Lower!"
        else: 
            guess_result = "Correct!"
    elif guess_int != secret_number:
        guess_result = "You ran out of guesses.  The number was " + secret_number
    else:
        guess_result = "Correct!" # win in the last run.

    print guess_result
    print
    
    # Start new game immediately if player wins or loses.
    if guess_result == "Correct!" or remaining_attempts == 0:
        new_game()


    
# Create frame
frame = simplegui.create_frame("Guess the number", 200, 200)


# Register event handlers for control elements and start frame
frame.add_input("Your Guess", input_guess, 100)
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.start()

# Call new_game 
new_game()
