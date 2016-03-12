# Implementation of card game - Memory

# Author: Qisong Wang
# Last edit: 2015/10/16


# Libraries
import simplegui
import random


# Constants
CARD_NUMBER = 16
CARD_WIDTH = 50
CARD_HEIGHT = 100
NUMBER_SIZE = 50


# Helper function
def new_game():

    """ Initialise all global variables at the start of new games """

    # Global variables
    global cards
    global exposed
    global turn_counter
    global state
    global index1, index2

    # Create anc combine two same decks of cards and randomise their sequence
    cards = range(CARD_NUMBER // 2) + range(CARD_NUMBER // 2)
    random.shuffle(cards)

    # Cover all cards at the beginning
    exposed = [False] * CARD_NUMBER

    # Clear counter, state number, and indices
    turn_counter = 0
    label.set_text("Turns = " + str(turn_counter))
    state = 0
    index1 = 0
    index2 = 0


# Event handlers
def mouseclick(pos):

    """ Mouse click handler containing game logics"""

    global state
    global turn_counter
    global index1, index2

    # Know which card is clicked
    i = pos[0] // CARD_WIDTH

    # Expose the clicked card at the begining
    # remember it as the first card in a run
    # start to count number of turns
    # and turn to state 1 next click
    if state == 0:
        exposed[i] = True
        index1 = i
        turn_counter += 1
        state = 1
    # If a second unexposed card is clicked,
    # remember it, jump to state 2 next click
    # otherwise, stay in state 1
    elif state == 1:
        if not exposed[i]:
            exposed[i] = True
            index2 = i
            state = 2
    # If a new unexposed card is clicked,
    # compare the previous 2 cards,
    # hide them again if they do not pair,
    # else, keep them exposed,
    # start a new turn, and make the new
    # card the first card in this turn.
    else:
        if not exposed[i]:
            exposed[i] = True
            if  cards[index1]!= cards[index2]:
                exposed[index1] = False
                exposed[index2] = False
            index1 = i
            state = 1
            turn_counter += 1

    # Update number of turns
    label.set_text("Turns = " + str(turn_counter))


def draw(canvas):

    """ draw canvas objects:
        cards are logically 50x100 pixels in size """

    # Draw cards on the canvas
    for i in range(len(cards)):
        canvas.draw_text(str(cards[i]), [i*CARD_WIDTH+NUMBER_SIZE*0.25,CARD_HEIGHT/2+NUMBER_SIZE*0.3], NUMBER_SIZE, 'White');
        # If one card not exposed, cover it with a rectangle
        if not exposed[i]:
            upper_left = [i*CARD_WIDTH, 0]
            upper_right = [(i+1)*CARD_WIDTH, 0]
            lower_right = [(i+1)*CARD_WIDTH, CARD_HEIGHT]
            lower_left = [i*CARD_WIDTH, CARD_HEIGHT]
            canvas.draw_polygon([upper_left, upper_right, lower_right, lower_left], 1, 'Black', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CARD_WIDTH * CARD_NUMBER, CARD_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


# get things rolling
new_game()
frame.start()
