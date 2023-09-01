# project5_model - this is where all of the static global variables are contained.


#   The width and height of the intial window is 600 x 1200

INITIAL_WIDTH = 600
INITIAL_HEIGHT = 1200



#   These are the static color variables that are used throughout the game,
#   either for elements of the interface such as the title and background,
#   or other elements such as jewels. Since jewels are noted with uppercase
#   letters in the game logic module, I have named the related colors as
#   ?_COLOR, where the ? denotes the uppercase letter that resembles the jewel.

S_COLOR = (255, 0, 0)           # red
T_COLOR = (252, 111, 3)         # orange
V_COLOR = (252, 236, 3)         # yellow
W_COLOR = (24, 252, 3)          # neon green
X_COLOR = (5, 250, 234)         # neon blue
Y_COLOR = (0, 12, 250)          # dark blue
Z_COLOR = (187, 0, 250)         # violet
BG_COLOR = (20, 20, 20)         # dark grey
JEWEL_OUTLINE = (25, 25, 25)    # light grey
WHITE = (235, 235, 235)         # white



#   Below are the fractional coordinates of the many elements of the game.
#   The X and Y attributes denote the fractional x and y coordinate of the
#   top left point of an images positional rectangle, respectively. The WIDTH and
#   HEIGHT attributes denote the fractional width and height of the positional
#   rectangles, respectively.

JEWEL_FRAC_WIDTH = 0.083335         
JEWEL_FRAC_HEIGHT = 0.0666667       
JEWEL_FRAC_X = 0.5
JEWEL_FRAC_Y = 0.13333

TITLE_FRAC_HEIGHT = 0.133334        
TITLE_FRAC_X = 0.015                
TITLE_FRAC_Y = 0.0                  

GAMEOVER_FRAC_X = 0.015             
GAMEOVER_FRAC_Y = 0.455             
GAMEOVER_FRAC_HEIGHT = 0.06         

SCORE_TITLE_FRAC_X = 0.06
SCORE_TITLE_FRAC_Y = 0.225
SCORE_IMAGE_FRAC_WIDTH = 0.4
SCORE_IMAGE_FRAC_HEIGHT = 0.05
SCORE_COUNT_FRAC_X = 0.164
SCORE_COUNT_FRAC_WIDTH = 0.15
SCORE_COUNT_FRAC_HEIGHT = 0.04
SCORE_COUNT_FRAC_Y = 0.275

NEXT_FALLER_FRAC_X = 0.1925
NEXT_FALLER_FRAC_Y = 0.525
NEXT_FALLER_IMAGE_FRAC_WIDTH = 0.4
NEXT_FALLER_IMAGE_FRAC_HEIGHT = 0.05
NEXT_FALLER_TITLE_FRAC_X = 0.052
NEXT_FALLER_TITLE_FRAC_Y = 0.45

BORDER_FRAC_WIDTH = 0.49
BORDER_FRAC_HEIGHT = 0.13

FINAL_SCORE_FRAC_WIDTH = 0.305
FINAL_SCORE_FRAC_HEIGHT = 0.55
FINAL_SCORE_FRAC_X = 0.4185
FINAL_SCORE_FRAC_Y = 0.6
