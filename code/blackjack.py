# Mini-project #6 - Blackjack

# Author: Qisong Wang
# Last edit: 2015/10/22


# Libraries
import simplegui
import random


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")


# initialize some useful global variables
in_play = False
outcome = ""
instruction = ""
score = 0
deck = []
player = []
dealer = []


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for card in self.cards:
            ans += str(card.get_suit()) + str(card.get_rank()) + " "
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        number_of_A = 0
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                number_of_A += 1
        if number_of_A == 1 and (value + 10) < 21:
            value += 10
        return value

    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        card = self.cards.pop()
        return card

    def __str__(self):
        ans = "Deck contains "
        for card in self.cards:
            ans += card.get_suit() + card.get_rank() + " "
        return ans


#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, player, dealer

    # Lower score for giving up last deal
    if in_play:
        outcome = "Score -1 for giving up"
        score -= 1

    # (Re)create deck and hands
    deck = Deck()
    player = Hand()
    dealer = Hand()
    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    in_play = True


def hit():
    global outcome, in_play, score
    global deck, player, dealer

    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = "You went busted and you lose"
            in_play = False
            score -= 1


def stand():
    global outcome, in_play, score
    global deck, player, dealer

    if in_play:
        if player.get_value() > 21:
            outcome = "You have busted and you lose"
            score -= 1
        else:
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "Dealer went busted and you win"
                score += 1
            else:
                if player.get_value() > dealer.get_value():
                    outcome = "You win"
                    score += 1
                else:
                    outcome = "You lose"
                    score -= 1

    in_play = False


# draw handler
def draw(canvas):
    global outcome, in_play, instruction
    global deck, player, dealer

    # Draw cards in hands
    dealer.draw(canvas, [100, 200])
    player.draw(canvas, [100, 400])

    # Hide dealer's first card if in play
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
        instruction = "Hit or Stand?"
    else:
        instruction = "New deal?"

    canvas.draw_text("Blackjack", [200, 100], 50, 'Red')
    canvas.draw_text("Dealer", [100, 180], 20, 'Black')
    canvas.draw_text("Player", [100, 380], 20, 'Black')
    canvas.draw_text(outcome, [300, 180], 20, 'Black')
    canvas.draw_text(instruction, [300, 380], 20, 'Black')
    canvas.draw_text(("Score: " + str(score)), [450, 100], 20, 'Blue')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
