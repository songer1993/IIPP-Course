# Pong Game

# Author: Qisong Wang
# Last edit: 2015/10/01

# This is an arcade game: Pong


# Modules
import simplegui
import random


# Globals 
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
REFRESH_RATE = 60 # Screen refresh rate 60 Hz
PAD_SPEED = 5 # Paddle moving speed
strike_counter = 0
ADD_DIFFICULTY = 0.2 # Add 20% ball movement speed every strike
score1 = 0
score2 = 0


# Helpler function
def spawn_ball(direction):
    """ initialize ball_pos and ball_vel for new bal in middle of table
        if direction is RIGHT, the ball's velocity is upper right, else upper left. """
    
    global ball_pos, ball_vel # these are vectors stored as lists
    global strike_counter
    
    # clear strike counter each new run
    strike_counter = 0
    
    # determine new initial velocity
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / REFRESH_RATE, -random.randrange(60, 180) / REFRESH_RATE]
    elif direction == LEFT:
        ball_vel = [-random.randrange(120, 240) / REFRESH_RATE, -random.randrange(60, 180) / REFRESH_RATE]

        
# Event handlers
def new_game():
    """ Start a new game at the beginning or when 'Restart' button is pressed. """
   
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # initialise the positons, velocity of paddles, and scores of players.
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    # spawn the ball in the centre
    if random.randrange(0,2):
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

    
def draw(canvas):
    """ draw objects and texts """
    
    global score1, score2, strike_counter, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball's position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # update ball's vertical velocity
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS :
        ball_vel[1] = -ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel < 0 :
        paddle1_pos = HALF_PAD_HEIGHT
    elif HEIGHT - (paddle1_pos + HALF_PAD_HEIGHT + paddle1_vel) < 0 :
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
        
    if (paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel < 0):
        paddle2_pos = HALF_PAD_HEIGHT
    elif HEIGHT - (paddle2_pos + HALF_PAD_HEIGHT + paddle2_vel) < 0 :
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    paddle1_left = 0
    paddle1_right = PAD_WIDTH
    paddle1_top = paddle1_pos - HALF_PAD_HEIGHT
    paddle1_bottom = paddle1_pos + HALF_PAD_HEIGHT
    paddle2_left = WIDTH - PAD_WIDTH
    paddle2_right = WIDTH
    paddle2_top = paddle2_pos - HALF_PAD_HEIGHT
    paddle2_bottom = paddle2_pos + HALF_PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([[paddle1_left,paddle1_top], [paddle1_right, paddle1_top], [paddle1_right, paddle1_bottom], [paddle1_left,paddle1_bottom]], 0.1, "Black", "White") 
    canvas.draw_polygon([[paddle2_left,paddle2_top], [paddle2_right, paddle2_top], [paddle2_right, paddle2_bottom], [paddle2_left,paddle2_bottom]], 0.1, "Black", "White") 

    # determine whether paddle and ball collide,
    # if collide, increase the ball's speed
    # otherwise, increment the score of the other player
    # and respawn a ball in the centre.
    if ball_pos[0] <= (paddle1_right+BALL_RADIUS) :
        if (ball_pos[1] >= paddle1_top) and (ball_pos[1] <= paddle1_bottom) :
            ball_vel[0] = -ball_vel[0]
            strike_counter += 1
            ball_vel[0] = ball_vel[0] * (1 + ADD_DIFFICULTY)
            ball_vel[1] = ball_vel[1] * (1 + ADD_DIFFICULTY)
        else:
            spawn_ball(RIGHT)
            score2 += 1
     
    elif (ball_pos[0] >= (paddle2_left-BALL_RADIUS)) :
        if (ball_pos[1] >= paddle2_top) and (ball_pos[1] <= paddle2_bottom) : 
            ball_vel[0] = -ball_vel[0]
            strike_counter += 1
            ball_vel[0] = ball_vel[0] * (1 + ADD_DIFFICULTY)
            ball_vel[1] = ball_vel[1] * (1 + ADD_DIFFICULTY)
        else:
            spawn_ball(LEFT)
            score1 += 1
            
    # draw scores
    canvas.draw_text(str(score1), [0.22*WIDTH, 0.2*HEIGHT], 50, "White")
    canvas.draw_text(str(score2), [0.75*WIDTH, 0.2*HEIGHT], 50, "White")

    
        
def keydown(key):
    """ if key is pressed down, assign a speed to the paddle
        according to the key pressed """
    
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_SPEED
    else:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED
    else:
        paddle2_vel = 0
                            

def keyup(key):
    """ Clear the speed of the paddle when the key
        is released """
    
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button_newgame = frame.add_button("Restart", new_game, 150)


# start frame
new_game()
frame.start()
