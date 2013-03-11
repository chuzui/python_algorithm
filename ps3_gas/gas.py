# gas.py
# Authors: Ronald L. Rivest, Michael Lieberman, Erik Demaine
# Date: March 6, 2008
# Gas simulation (aka bouncing colored balls)
# Uses PyGame for graphics (see www.pygame.org)

###########################################################################
### License stuff                                                       ###
###########################################################################
"""
Copyright (C) 2006  Ronald L. Rivest
Copyright (C) 2008  Erik Demaine and Michael Liberman

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.

[Note: the pygame library, upon which this is based, comes with the
 Lesser GPL license (LGPL).]
"""
###########################################################################
###########################################################################

import math
import random
import time
import sys

# Global constants:

# coordinates of "walls" of world
# world_min_x = -1414.0            # minimum x in world coordinates
# world_max_x = +1414.0            # maximum x in world coordinates
# world_min_y = -1414.0            # minimum y in world coordinates
# world_max_y = +1414.0            # maximum y in world coordinates

ball_min_radius = 16.0           # minimum radius for ball (world units)
ball_max_radius = 128.0          # maximum radius for ball

#The number of balls will be a number in this list
number_balls_list = [0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,40,50,75,100,
                     125,150,200,250,300,350,400,450,500,600,700,800,
                     900,1000,1200,1400,1600,1800,2000]

# Global variables:

balls = []                       # list of balls
number_balls = 200               # number of balls
speed = 24.0                     # world units per simulation step
infrequent_display = False       # True if ball shown only once/second or so
                                 #    ('d' flips this), to save CPU time
                                 # -- automatically on if no GUI
autopause_period = 1000          # How often to pause automatically
                                 # (0 if never)
paused = False                   # True if steps are running
total_collisions = 0             # total collisions counted
total_steps = 0                  # total simulation steps
full_screen = False              # Full-screen pygame video mode?

###########################################################################
### Graphical display related stuff                                     ###
###########################################################################

GUI_NONE = 0
GUI_PYGAME = 1
GUI_TKINTER = 2
gui = GUI_NONE
try:
    import pygame
    #from pygame.locals import *
    gui = GUI_PYGAME

    pygame_keymap = {
         pygame.K_ESCAPE: 'Escape',
         pygame.K_F1: 'F1',
         pygame.K_LEFT: 'Left',
         pygame.K_RIGHT: 'Right',
         pygame.K_UP: 'Up',
         pygame.K_DOWN: 'Down',
         pygame.K_c: 'c',
         pygame.K_d: 'd',
         pygame.K_p: 'p',
         pygame.K_SPACE: 'space',
         pygame.K_RETURN: 'Return',
         pygame.K_PAGEUP: 'Prior',
         pygame.K_PAGEDOWN: 'Next',
    }
except ImportError:
    try:
        import Tkinter
        ## no actual Tkinter support yet; coming soon hopefully
        gui = GUI_TKINTER
    except ImportError:
        pass
## Turn off GUI if you want:
#gui = GUI_NONE

## screen coordinates are (0,0) at upper left
##   x coordinates increase to right
##   y coordinates increase down

# global constants 

White = (250,250,250)
Black = (0,0,0)

# global variables 

screen_size_x = 800     # window size, possibly set later to full-screen size
screen_size_y = 600     # (measured in pixels)

color_scheme = 1                 # 0 = white background, 1 = black background
background_color = Black
line_color = White

#pixel_size = 9.0                 # size of pixel in world coordinates
screen_center_x = 0.0            # center of screen in world coordinates
screen_center_y = 0.0            # center of screen in world coordinates

def convert_to_pixels(x,y):
    """
    Return x and y coordinates (given in world units) to screen coords.
    """
    xs = int((x - screen_center_x)/pixel_size + screen_size_x//2)
    ys = int((y - screen_center_y)/pixel_size + screen_size_y//2) #- 20
    return (xs,ys)

def tkcolor(color):
    return '#%02x%02x%02x' % tuple(color)

# procedures

def set_color_scheme(scheme):
    """ 
    Set color scheme. 
      138    0.003    0.000    0.006    0.000 gas.py:449(vdot)
    scheme = 0 (white background) or 1 (black background)
    """
    global line_color, background_color
    if scheme == 0:
        line_color = Black
        background_color = White
    if scheme == 1:
        line_color = White
        background_color = Black

class Ball:
    """ 
    Implements a point/ball
    """

    # number of balls that have been created
    count = 0

    def __init__(self):
        # Position attributes (floats):
          self.x = random.uniform(world_min_x,world_max_x)
          self.y = random.uniform(world_min_y,world_max_y)
        # Velocity attributes (floats):
          angle = random.uniform(0.0,2* math.pi)    #  direction of motion in radians
          ball_speed = random.uniform(0.0,2.0)      #  speed in world units/step
          self.vx = math.sin(angle) * ball_speed    #  x component of velocity in world units/step
          self.vy = math.cos(angle) * ball_speed    #  y component of velocity in world units/step
        # Radius (int):
          self.radius = int(random.uniform(ball_min_radius,ball_max_radius))  # in world units

        # Mass is proportional to area (float):
          self.mass = float(self.radius**2)         # in (world units)**2 units (arbitrary)
        # Color (in RGB) is randomly chosen
          self.color = [120+int(random.random()*130),     
                        120+int(random.random()*130),
                        120+int(random.random()*130)]
        # ID, unique to the ball
          self.id = Ball.count
          Ball.count += 1
        # Tkinter needs to keep track of the balls.
          self.gui_object = None

    def __hash__(self):
        return self.id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def draw(self,surface):
        """ 
        Draw ball.         
        """
        global pixel_size

        # center and radius in pixel coords
        (xs,ys) = convert_to_pixels(self.x,self.y)
        rs = int(self.radius/pixel_size)

        # return if ball surely can't be seen
        #if xs+rs<0: return
        #if xs-rs>screen_size_x: return
        #if ys+rs<0: return
        #if ys-rs>screen_size_y:return

        if gui == GUI_TKINTER:
            color = tkcolor(self.color)
            if self.gui_object is None:
                self.gui_object = surface.create_oval((xs-rs,ys-rs,xs+rs,ys+rs),
                                                      fill=color)
            else:
                surface.coords(self.gui_object, (xs-rs,ys-rs,xs+rs,ys+rs))
                surface.itemconfig(self.gui_object, fill=color)

        elif gui == GUI_PYGAME:
            # draw colored inside portion
            pygame.draw.circle(surface,
                               self.color,
                               [xs,ys],
                               rs,
                               0)  # width (0 means fill circle)
            # draw circumference
            # pygame.draw.circle(surface,
            #                    line_color,
            #                    [xs,ys],
            #                    rs,
            #                    min(1,rs))  # width

def initialize():
    """ 
    Initialize GUI (e.g. pygame) and set up display screen, background, etc. 
    """
    global screen, statusbar, background, font, screen_size_x, screen_size_y

    if gui == GUI_TKINTER:
        screen = Tkinter.Tk()
        screen.wm_title('Gas simulation program')
        #font = tkFont.Font(size=36)
        statusbar = Tkinter.Label(screen)
        statusbar.pack(side='bottom', fill='x')
        background = Tkinter.Canvas(screen,
            width=screen_size_x, height=screen_size_y)
        background.pack(side='bottom')

    elif gui == GUI_PYGAME:
        pygame.init()
        pygame.display.set_caption('Gas simulation program')

        if full_screen:
            # get size of fullscreen display into screen_size_x, screen_size_y
            modes = pygame.display.list_modes()    # defaults to fullscreen
            modes.sort()                           # largest goes last
            screen_size_x,screen_size_y = modes[-1]

            screen = pygame.display.set_mode((screen_size_x, screen_size_y),
                                             pygame.FULLSCREEN )
        else:
            screen = pygame.display.set_mode((screen_size_x,screen_size_y))

        pygame.key.set_repeat(500,300)   # for handling key repeats

        font = pygame.font.Font(None, 36)

        background = pygame.Surface(screen.get_size())
        background = background.convert()

def set_background_color(color):
    """
    Fill background pattern with specified background color.
    """
    global background

    if gui == GUI_TKINTER:
        background['background'] = tkcolor(color)

    elif gui == GUI_PYGAME:
        background.fill(color)

def show_background():
    """ 
    Blit background onto screen and show it. 
    """
    global background, screen

    if gui == GUI_TKINTER:
        screen.update()

    elif gui == GUI_PYGAME:
        screen.blit(background, (0, 0))
        pygame.display.flip()


def show_text_screen(msgs, welcome=False, help=False):
    """ 
    Show a screen of text.
    Return True if user wishes to quit out of this text screen.
    """
    global font, background, paused, number_balls, autopause_period

    def ball_text():
        """
        Draw a text object for the number of balls.
        """
        balltext = font.render("Number of balls (UP/DOWN):  " +
                               "%d" % number_balls,
                               1,
                               Black)
        balltextpos = balltext.get_rect()
        balltextpos.centerx = background.get_rect().centerx
        balltextpos.centery = 420
        pygame.draw.rect(background, White, balltextpos.inflate(1000, 0))
        background.blit(balltext, balltextpos)

    def autopause_text():
        """
        Draw a text object for the autopause period.
        """
        pausetext = None
        if autopause_period == 0:
            pausetext = font.render("Automatically pause (PGUP/PGDN):  Never",
                                    1,
                                    Black)
        else:
            pausetext = font.render("Automatically pause (PGUP/PGDN):  " +
                                    "every %d timesteps" % autopause_period,
                                    1,
                                    Black)
        pausetextpos = pausetext.get_rect()
        pausetextpos.centerx = background.get_rect().centerx
        pausetextpos.centery = 460
        pygame.draw.rect(background, White, pausetextpos.inflate(1000, 0))
        background.blit(pausetext, pausetextpos)

    set_background_color(White)

    y = 100                               # starting y coord, for first line
    objects = []
    for msg in msgs:
        if gui == GUI_TKINTER:
            objects.append(background.create_text(screen_size_x//2,y,
                text=msg))
        elif gui == GUI_PYGAME:
            text = font.render(msg, 
                               1,             # antialias
                               Black)         # color
            textpos = text.get_rect()
            textpos.centerx = screen_size_x//2
            textpos.centery = y
            background.blit(text, textpos)
        y += 40

    if welcome:
        if gui != GUI_PYGAME: return
        ball_text()
        autopause_text()

    # Now wait for user to hit a key, before proceeding.
    # Check if keypress indicates user wants to quit, and if so return True
    while True:
        show_background()
        for key in keyboard():
            if key == 'Escape':
                return True
            elif key == 'space' or key == 'Return' or (key == 'F1' and help):
                paused = False
                if gui == GUI_TKINTER:
                    for object in objects:
                        background.delete(object)
                return
            elif key == 'F1':
                return show_help_screen()
            elif welcome:
                if key == 'Down':
                    if number_balls in number_balls_list:
                        i = number_balls_list.index(number_balls)
                    else:
                        i = 0
                    i = max(0,i-1)
                    number_balls = number_balls_list[i]
                    ball_text()
                elif key == 'Up':
                    if number_balls in number_balls_list:
                        i = number_balls_list.index(number_balls)
                    else:
                        i = len(number_balls_list)-1
                    i = min(len(number_balls_list)-1,i+1)
                    number_balls = number_balls_list[i]
                    ball_text()
                elif key == 'Next':  # page down
                    if autopause_period == 0:
                        autopause_period = 65536
                    elif autopause_period < 10:
                        autopause_period = 0
                    else:
                        autopause_period /= 2
                    autopause_text()
                elif key == 'Prior':  # page up
                    if autopause_period == 0:
                        autopause_period = 8
                    elif autopause_period > 65536:
                        autopause_period = 0
                    else:
                        autopause_period *= 2
                    autopause_text()

def show_welcome_screen():
    """ 
    Show initial welcome / help screen. 
    """
    global number_balls, autopause_period, keybuffer

    msgs = ["gas.py -- gas simulation program",
            " ",
            "F1 at any time shows a help screen",
            "ESC at any time quits the program",
            "SPACE/ENTER starts the program",
            " ",
            "[GPL License]",
            ]

    if gui == GUI_NONE:
        print msgs[0] + \
              '  (no GUI enabled; install Tkinter or pygame if you want a GUI)'
        number_balls = int(raw_input('Number of balls: '))
        assert number_balls > 0
        autopause_period = int(raw_input(
            'Automatically pause every how many timesteps (0 = never): '))
        assert autopause_period >= 0

    elif gui == GUI_PYGAME:
        return show_text_screen(msgs, welcome=True)

    elif gui == GUI_TKINTER:
        #show_text_screen(msgs, welcome=True)
        inputs = Tkinter.Frame(screen)
        inputs.pack(side='top', fill='x')
        start = Tkinter.Button(inputs, text='Start\nSimulation', justify='center')
        start.pack(side='right', fill='both')
        inputs1 = Tkinter.Frame(inputs)
        inputs1.pack(side='top')
        Tkinter.Label(inputs1, text='Number of balls:').pack(side='left')
        number_balls_entry = Tkinter.Entry(inputs1)
        number_balls_entry.pack(side='left')
        number_balls_entry.insert(0, str(number_balls))
        inputs2 = Tkinter.Frame(inputs)
        inputs2.pack(side='top')
        Tkinter.Label(inputs2, text='Automatically pause every').pack(side='left')
        autopause_period_entry = Tkinter.Entry(inputs2)
        autopause_period_entry.pack(side='left')
        autopause_period_entry.insert(0, str(autopause_period))
        Tkinter.Label(inputs2, text='timesteps (0 = never)').pack(side='left')

        start.bind('<Button>', lambda event: screen.quit())
        while True:
            screen.mainloop()
            try:
                number_balls = int(number_balls_entry.get())
            except ValueError:
                continue
            try:
                autopause_period = int(autopause_period_entry.get())
            except ValueError:
                continue
            if number_balls > 0 and autopause_period >= 0:
                break
        start.unbind('<Button>')

        number_balls_entry['state'] = Tkinter.DISABLED
        start['state'] = Tkinter.DISABLED
        autopause_period_entry['state'] = Tkinter.DISABLED
        keybuffer = []
        screen.bind_all('<Key>', lambda event: keybuffer.append(event.keysym))

def show_help_screen():
    """ 
    Show help screen. 
    Return True if user wishes to quit out of help screen.
    """

    msgs = [#"Up arrow increases number of balls",
            #"Down arrow decreases number of balls",
            #" ",
            "Right arrow increases ball speed",
            "Left arrow decreases ball speed",
            "d toggles whether to frequently update the display",
            "p (un)pauses (with automatic pauses every 500 steps)",
            " ",
            "PAGEUP zooms out",
            "PAGEDOWN zooms in",
            " ",
            "c flips background color (black/white)",
            " ",
            "SPACE/ENTER proceeds",
            "F1 shows this help screen",
            "ESC quits"
            ]

    return show_text_screen(msgs, help=True)

last_step_time = time.time()        # when last simulation step started
last_display_time = time.time()     # when state was last displayed
steps_per_second = 10.0             # initial value only
seconds_per_step = 0.1
border = None
background = None

def display_balls(balls):
    """ 
    Show all balls.
    """
    global background, screen, border

    # draw line around world
    line_width = 2
    (xs_min,ys_min) = convert_to_pixels(world_min_x,world_min_y)
    (xs_max,ys_max) = convert_to_pixels(world_max_x,world_max_y)

    if gui == GUI_TKINTER:
        if border is None:
            border = background.create_rectangle(xs_min,ys_min,xs_max,ys_max,
                         outline=tkcolor(line_color), width=line_width)
        else:
            background.coords(border, xs_min,ys_min,xs_max,ys_max)
            background.itemconfigure(border, outline=tkcolor(line_color),
                                             width=line_width)
    elif gui == GUI_PYGAME:
        pygame.draw.line(background,line_color,(xs_min,ys_min),(xs_min,ys_max),line_width)
        pygame.draw.line(background,line_color,(xs_max,ys_min),(xs_max,ys_max),line_width)
        pygame.draw.line(background,line_color,(xs_min,ys_min),(xs_max,ys_min),line_width)
        pygame.draw.line(background,line_color,(xs_min,ys_max),(xs_max,ys_max),line_width)

    # draw balls
    for b in balls:
        b.draw(background)

def display_label():
    global steps_per_second, line_color, balls, background, last_step_time, \
           paused, statusbar, screen

    pausestring = "pause"
    if paused:
        pausestring = "resume"

    if gui == GUI_NONE:
        print '%d balls, %d collisions, step %d, %0.1f simulation steps / second' % \
            (len(balls), total_collisions, total_steps, steps_per_second)

    elif gui == GUI_TKINTER:
        statusbar['text'] = \
            '(F1/help, ESC/quit, P/%s)\n' % pausestring + \
            '%d balls, %d collisions, step %d, %0.1f simulation steps / second' % \
            (len(balls), total_collisions, total_steps, steps_per_second)

    elif gui == GUI_PYGAME:
        text1 = font.render("(F1/help, ESC/quit, P/" + pausestring + ")        " +
                            "%d balls         "%len(balls)+
                            "%d collisions"%total_collisions,
                            1,
                            line_color)
        text2 = font.render("Step %d                "%total_steps+
                            "%0.1f simulation steps / second"%steps_per_second,
                            1,
                            line_color)
        text1pos = text1.get_rect()
        text1pos.centerx = background.get_rect().centerx
        text1pos.centery = screen_size_y - 60
        text2pos = text2.get_rect()
        text2pos.centerx = background.get_rect().centerx
        text2pos.centery = screen_size_y - 30

        background.blit(text1,text1pos)
        background.blit(text2,text2pos)

###########################################################################
### USER INPUT                                                          ###
###########################################################################

def keyboard():
    if gui == GUI_TKINTER:
        while keybuffer:
            key = keybuffer[0]
            del keybuffer[0]
            yield key

    elif gui == GUI_PYGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                yield pygame_keymap[pygame.K_ESCAPE]
            elif event.type == pygame.KEYDOWN:
                if event.key in pygame_keymap:
                    yield pygame_keymap[event.key]

def handle_user_input():
    """ 
    Detect keypresses, etc., and handle them. 
    Return True iff user requests program to quit
    """
    global number_balls, balls, speed, screen_size_x, screen_size_y
    global color_scheme, infrequent_display, paused, pixel_size, keybuffer

    if gui == GUI_NONE:
        if not paused: return
        while True:
            choice = raw_input('Un(p)ause or (q)uit: ')
            if choice.lower().startswith('p'):
                paused = not paused
                return
            elif choice.lower().startswith('q'):
                return True

    for key in keyboard():
        if key == 'Escape':
            return True
        elif key == 'F1':
            if show_help_screen():
                return True
        #elif key == 'Down':
        #    if number_balls in number_balls_list:
        #        i = number_balls_list.index(number_balls)
        #    else:
        #        i = 0
        #    i = max(0,i-1)
        #    number_balls = number_balls_list[i]
        #    balls = balls[:number_balls]
        #elif key == 'Up':
        #    if number_balls in number_balls_list:
        #        i = number_balls_list.index(number_balls)
        #    else:
        #        i = len(number_balls_list)-1
        #    i = min(len(number_balls_list)-1,i+1)
        #    number_balls = number_balls_list[i]
        #    while len(balls)<number_balls:
        #        balls.append(Ball())
        elif key == 'Left':
            speed /= 1.4
        elif key == 'Right':
            speed *= 1.4
            speed = min(speed,screen_size_x/3,screen_size_y/3)
        elif key == 'c':
            color_scheme = (1+color_scheme)%2
            set_color_scheme(color_scheme)
        elif key == 'p' or key == 'space' or key == 'Return':
            paused = not paused
        elif key == 'd':
            infrequent_display = not infrequent_display
        elif key == 'Prior':  # page-up
            pixel_size *= 1.414
        elif key == 'Next':  # page-down
            pixel_size = pixel_size / 1.414

###########################################################################
### Routines related to ball motion and collision handling              ###
###########################################################################

def dist(b1,b2):
    """ 
    Return distance (in world units) between balls b1 and b2. 
    """
    return (math.sqrt((b1.x-b2.x)**2 + (b1.y-b2.y)**2))

def move_balls():
    """ 
    Move all balls. This is one 'simulation step', aside from
    detecting and handling collisions.
    """
    global balls
    for b in balls:
        move_ball(b)

def move_ball(b):
    """ 
    Move ball b one step, and bounce off edge of world.
    """
    global speed, world_min_x, world_max_x, world_min_y, world_max_y

    b.x += b.vx * speed
    b.y += b.vy * speed

    r = b.radius

    left = world_min_x
    if b.x < left + r:   # bounce off left wall
        b.x = (left + r)+(left+r-b.x)
        b.vx = -b.vx

    right = world_max_x
    if b.x > right - r:  # bounce off right wall
        b.x = (right - r)-(b.x-right+r)
        b.vx = -b.vx

    bottom = world_min_y
    if b.y < bottom + r: # bounce off bottom wall
        b.y = (bottom + r)+(bottom+r-b.y)
        b.vy = -b.vy

    top = world_max_y
    if b.y > top - r:    # bounce off top wall
        b.y = top - r-(b.y-(top-r))
        b.vy = -b.vy

### Vector operations

def vadd(v1,v2):
    """ Return sum of vectors v1 and v2. """
    return [a+b for a,b in zip(v1,v2)]

def vsub(v1,v2):
    """ Return vector v1-v2 """
    return [a-b for a,b in zip(v1,v2)]

def vscale(s,v):
    """ Return product of vector v by the scalar s. """
    return [s*a for a in v]

def vlensq(v):
    """ Return the length squared of vector v. """
    return sum([x*x for x in v])

def vlen(v):
    """ Return the length of vector v. """
    return math.sqrt(vlensq(v))

def vdot(v1,v2):
    """ Return the dot product of vectors v1 and v2. """
    return sum([a*b for a,b in zip(v1,v2)])

def vunit(v):
    """ Return unit vector in same direction as v. """
    length = vlen(v)
    assert length > 0.0
    return vscale(1.0/length,v)

################################################
## COLLISION DETECTION AND COLLISION HANDLING ##
################################################

class ball_pair:
    """
    Unordered pair of balls. Two ball_pairs are the same if they
    contain the same balls. Upon creation, the ball with the lower id
    is saved as self.b1, and the ball with the higher id is saved as
    self.b2.
    """
    
    def __init__(self, b1, b2):
        if b1 < b2:
            self.b1 = b1
            self.b2 = b2
        else:
            self.b1 = b2
            self.b2 = b1

    def __hash__(self):
        return int((hash(self.b1) + 1000003*hash(self.b2)) % 2**30)

    def __cmp__(self, other):
        if self.b1 != other.b1:
            return cmp(self.b1, other.b1)
        else:
            return cmp(self.b2, other.b2)

def detect_collisions(balls):
    """
    Detect any pairs of balls that are colliding.
    Returns a set of ball_pairs.
    """

    set_of_collisions = set()

    for i in range(len(balls)):
        b1 = balls[i]
        for j in range(i):
            b2 = balls[j]
            if colliding(b1, b2):
                set_of_collisions.add(ball_pair(b1, b2))

    return set_of_collisions

# Uncomment the line below to override detect_collisions with your version.
########################################
from detection import detect_collisions
########################################

def colliding(b1, b2):
    """
    Returns true if b1 and b2 are currently colliding.
    Returns false otherwise.
    """
    return dist(b1,b2) <= b1.radius + b2.radius

def handle_collisions(set_of_collisions):
    """
    Sorts collisions, and then handles them in that fixed order.
    """
    list_of_collisions = []
    for collision in set_of_collisions:
        list_of_collisions.append(collision)
    list_of_collisions.sort()
    for collision in list_of_collisions:
        handle_collision(collision.b1, collision.b2)

            
def handle_collision(b1,b2):
    """ 
    Collide balls b1 and b2.

    Net result is that velocities of b1 and b2 may be changed.
    Detects "false collisions" where balls are close but actually
    moving away from each other; in this case it does nothing.
    (This case is important if balls have just collided but
    haven't really moved apart yet.)
    This routine conserves energy and momentum.
    """
    global total_collisions
    total_collisions += 1

    # ball 1: mass, position, velocity
    m1 = b1.mass
    p1 = [b1.x,b1.y]
    v1 = [b1.vx,b1.vy]

    # ball 2: mass, position, velocity
    m2 = b2.mass
    p2 = [b2.x,b2.y]
    v2 = [b2.vx,b2.vy]

    # center of mass: position, velocity
    pc = vadd(vscale(m1/(m1+m2),p1),vscale(m2/(m1+m2),p2))
    vc = vadd(vscale(m1/(m1+m2),v1),vscale(m2/(m1+m2),v2))

    # return if at same position; can't do anything
    if p1 == p2: return

    u1 = vunit(vsub(p1,pc))      # unit vector towards m1 in cm coords
    w1 = vsub(v1,vc)             # velocity of m1 in cm coords
    z = vdot(w1,u1)              # amount of w1 in direction towards m1
    if z >= 0.0: return          # can't collide; m1 moving away from cm
    r1 = vscale(z,u1)            # velocity of m1 in cm coords along u1
    s1 = vsub(w1,vscale(2.0,r1)) # post-collision velocity in cm coords
    b1.vx, b1.vy = vadd(vc,s1)   # final velocity in global coords

    u2 = vunit(vsub(p2,pc))      # unit vector towards m2 in cm coords
    w2 = vsub(v2,vc)             # velocity of m2 in cm coords
    z = vdot(w2,u2)              # amount of w2 in direction towards m2
    if z >= 0.0: return          # can't collide; m2 moving away from cm
    r2 = vscale(z,u2)            # velocity of m2 in cm coords along u2
    s2 = vsub(w2,vscale(2.0,r2)) # post-collision velocity in cm coords
    b2.vx, b2.vy = vadd(vc,s2)   # final velocity in global coords


###########################################################################
### Main routine / event loop                                           ###
###########################################################################

def main():
    global number_balls, balls, infrequent_display, background_color, total_steps
    global last_display_time, steps_per_second, last_step_time, seconds_per_step
    global paused, world_max_y, world_min_y, world_max_x, world_min_x, pixel_size
    random.seed(17)

    initialize()
    set_background_color(background_color)
    
    if show_welcome_screen():
        return

    world_min_x = -200.0*number_balls**.5  # minimum x in world coordinates
    world_max_x = +200.0*number_balls**.5  # maximum x in world coordinates
    world_min_y = -200.0*number_balls**.5  # minimum y in world coordinates
    world_max_y = +200.0*number_balls**.5  # maximum y in world coordinates 
    pixel_size = 2 * world_max_y / min(screen_size_x,screen_size_y) 

    # Make initial set of balls
    balls = [Ball() for i in range(number_balls)]

    # Record what times we automatically paused, to prevent
    # neverending auto-pause.
    autopaused_on = {}

    # Event loop
    while True:  
        """ Each iteration of this loop is one 'simulation step'. """
        if handle_user_input(): return
        # auto-pause
        if total_steps > 0 and autopause_period > 0 and \
           total_steps % autopause_period == 0 and \
           not autopaused_on.has_key(total_steps):
            autopaused_on[total_steps] = True
            paused = True

        if not paused:
            total_steps += 1
            elapsed_step_time = time.time() - last_step_time  # since last step computed
            last_step_time = time.time()

            # seconds_per_step is computed as a moving average...
            seconds_per_step = 0.95 * seconds_per_step + 0.05*elapsed_step_time
            steps_per_second = 1.0 / seconds_per_step

            move_balls()
            handle_collisions(detect_collisions(balls))

        elapsed_display_time = time.time()-last_display_time
        if paused or not (infrequent_display or gui == GUI_NONE) \
                  or elapsed_display_time>2.0:
            last_display_time = time.time()
            set_background_color(background_color)
            display_balls(balls)
            display_label()
            show_background()

if __name__ == '__main__': 
    import optparse

    optparser = optparse.OptionParser()
    optparser.add_option('-n', '--none', help='use no GUI',
        action='store_const', dest='gui', const=GUI_NONE)
    optparser.add_option('-t', '--tk', '--tkinter', help='use Tkinter GUI',
        action='store_const', dest='gui', const=GUI_TKINTER)
    optparser.add_option('-p', '--pygame', help='use Pygame GUI',
        action='store_const', dest='gui', const=GUI_PYGAME)
    optparser.add_option('-b', '--balls', help='start with BALLS balls',
        action='store', type='int', dest='balls', metavar='BALLS')
    optparser.add_option('-a', '--autopause', help='autopause every PAUSE',
        action='store', type='int', dest='autopause', metavar='PAUSE')

    options, args = optparser.parse_args()
    if options.gui is not None: gui = options.gui
    if options.balls is not None: number_balls = options.balls
    if options.autopause is not None: autopause_period = options.balls
    
    # Profiling slows down the runtime by a significant factor.
    # We've turned it off to help you see the asymptotic behavior.
    # If you want to see profiling of the number of function calls
    # and how much time they take, you can uncomment the profiling lines.
    
    #import profile
    #profile.run("main()")
    main()
