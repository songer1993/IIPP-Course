# Stopwatch: The Game

# Author: Qisong Wang
# Last edit: 2015/09/26

# A stopwatch game where you could gain a point
# if you stop the watch on a whole second.


# Modules
import simplegui


# Global variables
STOPWATCH_FONT_SIZE = 100
GAMECOUNTER_FONT_SIZE = 50
CANVAS_LENGTH = 500
CANVAS_WIDTH = 400
COUNTER_MAX = 6000 # 10 minutes
counter = 0
counter_x = 0 # number of successful stops
counter_y = 0 # number of stops
stopwatch_running = False


# Helper fuctions
def format(t):
    """ Converts time in tenths of seconds into 
        formatted string A:BC.D """
    D = t % 10
    t = t / 10
    C = t % 10
    t = t / 10
    B = t % 6
    t = t / 6
    A = t % 10
    
    return str(A)+":"+str(B)+str(C)+"."+str(D)
    
    
# Event handlers
def stopwatch_start():
    """ Start stopwatch when 'Start' button pressed """
    global stopwatch_running
    
    #Start timer
    timer.start()
    stopwatch_running = True
    
    
def stopwatch_stop():
    """ Stop stopwatch when 'Stop' button pressed """
    global counter_x
    global counter_y
    global stopwatch_running
    
    # Stop timer first
    timer.stop()
    
    # Increment success/attempt counter 
    # only when the stopwatch is running
    if stopwatch_running == True:
        counter_y += 1
        if counter % 10 == 0:
            counter_x += 1
        
    stopwatch_running = False

    
    
def stopwatch_reset():
    """ Reset stopwatch when 'Reset' button pressed """
    global counter
    global counter_x
    global counter_y
    global stopwatch_running

    # Stop timer first
    timer.stop()
        
    # Reset all counters
    counter = 0
    counter_x = 0
    counter_y = 0
    stopwatch_running = False



def timer_handler():
    """ Timer with 0.1 sec interval """
    global counter
    
    counter += 1
    if counter == COUNTER_MAX:
        counter = 0
    

def draw_handler(canvas):
    """ Draw stopwatch and game counter """
    
    # Format messages
    stopwatch_message = format(counter)
    gamecounter_message = str(counter_x)+"/"+str(counter_y)
    # Compute appropriate text positions
    # according to the canvas size and font size
    center_x = round((CANVAS_LENGTH - 2.5*STOPWATCH_FONT_SIZE)/2)
    center_y = round((CANVAS_WIDTH + 0.5*STOPWATCH_FONT_SIZE)/2)
    upper_right_x = round(CANVAS_LENGTH-2*GAMECOUNTER_FONT_SIZE)
    upper_right_y = GAMECOUNTER_FONT_SIZE
    # Draw texts on the canvas
    canvas.draw_text(stopwatch_message, [center_x, center_y], STOPWATCH_FONT_SIZE, "White")
    canvas.draw_text(gamecounter_message, [upper_right_x, upper_right_y], GAMECOUNTER_FONT_SIZE, "Red")
    
    
# Create frame
frame = simplegui.create_frame("Stopwatch: The Game", CANVAS_LENGTH, CANVAS_WIDTH)


# Register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
start_button = frame.add_button("Start", stopwatch_start, 100)
stop_button = frame.add_button("Stop", stopwatch_stop, 100)
reset_button = frame.add_button("Reset", stopwatch_reset, 100)


# Start frame
frame.start()
