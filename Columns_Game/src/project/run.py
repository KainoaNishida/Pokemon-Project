# project5 - visual implementation of the columns game

import columns
import time
import pygame
from project5_model import *

class columns_game:
    def __init__(self):
        self._running = True
        self._gamestate = columns.GameState(columns.make_empty_field(13, 6), None, 0, columns.FALLING)
        self._gamestate.update_faller(self._gamestate.make_random_faller())
        self._next_faller = self._gamestate.make_random_faller()

    def run(self) -> None:
        pygame.init()

        
        clock = pygame.time.Clock()
        self._initialize_all_attributes()
        self._gamestate.handle_command('')
        
        while self._running:
            
            clock.tick(30)
            try:
                if self._gamestate.state() == columns.FALLING:

                    if self._handle_events() is True:
                         pass
                    else:
                        if self._faller_second == 0:
                            self._pass_time_and_reset_faller_second()
                            if self._gamestate.state() == columns.FROZEN:
                                self._thud()
                    self._draw()
                            
                else:
                    if self._faller_second == 0:
                        if columns.is_matching_possible(self._gamestate):
                                self._sparkle()
                                self._draw_white()
                                self._pass_time_and_reset_faller_second()
                        
                        elif self._gamestate.state() == columns.FROZEN:
                                self._reset_gamestate_after_faller_freezes()
                                self._pass_time_and_reset_faller_second()
                        else:
                                self._pass_time_and_reset_faller_second()
            except:
                self._running = False
                self._play_gameover_sound()
                self._draw_final_screen()
                time.sleep(3)
                
            self._faller_second -= 1
                
        pygame.quit()

    def _pass_time_and_reset_faller_second(self) -> None:
        'Passes time and then resets the faller_second timer'
        self._gamestate.handle_command('')
        self._faller_second = 30
        
        
    def _initialize_all_attributes(self) -> None:
        'Loads all of the external files and intitializes any necessary variables'
        self._create_surface((INITIAL_WIDTH, INITIAL_HEIGHT))
        self._font = pygame.font.Font(None, 50)
        self._thud_sound = pygame.mixer.Sound('fall_thud.mp3')
        self._gameover_sound = pygame.mixer.Sound('gameover_sound.wav')
        self._match_sound = pygame.mixer.Sound('sparkle.wav')
        self._title_image = pygame.image.load('title_image.png')
        self._gameover_image = pygame.image.load('gameover_image.png')
        self._score_image = pygame.image.load('score_image.png')
        self._next_faller_image = pygame.image.load('next_faller_image.png')
        self._score = 0
        self._title_image_scaled = None
        self._faller_second = 30
        
        
    def _draw_final_screen(self) -> None:
        'Draws the end screen'
        self._draw_gameover_title()
        self._draw_final_score()
        pygame.display.flip()

    def _draw_gameover_title(self) -> None:
        'Draws the gameover text'
        pixel_width, pixel_height = self._get_pixel_width_and_height()
        
        pixel_tl_x = GAMEOVER_FRAC_X * pixel_width
        pixel_tl_y = GAMEOVER_FRAC_Y * pixel_height

        self._surface.fill(pygame.Color(BG_COLOR))
        self._gameover_image_scaled = pygame.transform.scale(self._gameover_image, (pixel_width, GAMEOVER_FRAC_HEIGHT*pixel_height))
        self._surface.blit(self._gameover_image_scaled,(pixel_tl_x, pixel_tl_y))
        
    def _thud(self) -> None:
        'Sound for when fallers freeze'
        self._thud_sound.play()

    def _sparkle(self) -> None:
        'Sound for when jewels match'
        self._match_sound.play()
    
    def _play_gameover_sound(self) -> None:
        'Sound for when the game ends'
        self._gameover_sound.play()

    def _reset_gamestate_after_faller_freezes(self) -> None:
        '''Resets the gamestate after a faller freezes by setting the next faller
        (making sure the column is not one that is already filled unless all
         are filled, which raises a GameOverError), resetting the count, and
        updating the state to falling rather than Frozen.'''
        
        self._gamestate.handle_command('')
        
        if self._gamestate.check_if_board_is_full() == True:
            while columns.get_bottom_row(self._next_faller.column(), self._gamestate) == 0:
                self._next_faller.change_column()
        else:
            raise GameOverError
        
        self._gamestate.update_faller(self._next_faller)
        self._next_faller = self._gamestate.make_random_faller()
        self._gamestate.update_state(columns.FALLING)
        self._gamestate.update_count(0)

    def _handle_events(self) -> None:
        '''Handles all possible events, which are exiting the game, resizing the
        window, pressing the space key, pressing the right arrow key, and pressing
        the left arrow key'''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._gamestate.handle_command('<')
                    
                elif event.key == pygame.K_RIGHT:
                    self._gamestate.handle_command('>')
                    
                elif event.key == pygame.K_SPACE:
                    self._gamestate.handle_command('R')
                    
        
                    

    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)
        self._title_image_scaled = None

    def _draw(self) -> None:
        'Draws the entire playable game'
        self._surface.fill(pygame.Color(BG_COLOR))
        self._draw_next_faller()
        self._draw_board()
        self._draw_title()
        self._draw_score()
        self._draw_border()
        pygame.display.flip()

    def _draw_border(self) -> None:
        'Draws the borders that outline the playing field'
        pixel_width, pixel_height = self._get_pixel_width_and_height()

        pygame.draw.line(self._surface, pygame.Color(WHITE), (BORDER_FRAC_WIDTH * pixel_width, BORDER_FRAC_HEIGHT * pixel_height), (BORDER_FRAC_WIDTH * pixel_width, pixel_height), width = 2)
        pygame.draw.line(self._surface, pygame.Color(WHITE), (BORDER_FRAC_WIDTH * pixel_width, BORDER_FRAC_HEIGHT * pixel_height), (pixel_width, BORDER_FRAC_HEIGHT * pixel_height), width = 2)

    def _draw_score(self) -> None:
        'Draws the score while the game is in progress'
        pixel_width, pixel_height = self._set_scaled_score_and_count_image()
        self._surface.blit(self._score_image_scaled, (SCORE_TITLE_FRAC_X * pixel_width, SCORE_TITLE_FRAC_Y * pixel_height))
        self._surface.blit(self._score_count_scaled, (SCORE_COUNT_FRAC_X * pixel_width, SCORE_COUNT_FRAC_Y * pixel_height))

    def _draw_final_score(self) -> None:
        'Draws the score on the end screen'
        pixel_width, pixel_height = self._set_scaled_score_and_count_image()
        self._surface.blit(self._score_image_scaled, (FINAL_SCORE_FRAC_WIDTH * pixel_width, FINAL_SCORE_FRAC_HEIGHT * pixel_height))
        self._surface.blit(self._score_count_scaled, (FINAL_SCORE_FRAC_X * pixel_width, FINAL_SCORE_FRAC_Y * pixel_height))

    def _set_scaled_score_and_count_image(self) -> tuple[float, float]:
        '''Returns a tuple containg the width and height of the current surface,
        and sets scaled images for the score count and for the score text'''
        
        pixel_width, pixel_height = self._get_pixel_width_and_height()
        _score_count = self._font.render(f'{"{:03d}".format(self._score)}', True, pygame.Color(WHITE), pygame.Color(BG_COLOR))
        self._score_image_scaled = pygame.transform.scale(self._score_image, (SCORE_IMAGE_FRAC_WIDTH* pixel_width, SCORE_IMAGE_FRAC_HEIGHT*pixel_height))
        self._score_count_scaled = pygame.transform.scale(_score_count, (SCORE_COUNT_FRAC_WIDTH * pixel_width, SCORE_COUNT_FRAC_HEIGHT * pixel_height))
        return pixel_width, pixel_height

    def _draw_title(self) -> None:
        'Draws the title of the game'
        pixel_width, pixel_height = self._get_pixel_width_and_height()
        pixel_tl_x = TITLE_FRAC_X *self._surface.get_width()
        pixel_tl_y = TITLE_FRAC_Y

        self._title_image_scaled = pygame.transform.scale(self._title_image, (pixel_width, TITLE_FRAC_HEIGHT* pixel_height))
        self._surface.blit(self._title_image_scaled,(pixel_tl_x, pixel_tl_y))       
    
    def _draw_white(self) -> None:
        'If a board has matching jewels, draws those jewels as white'
        for row in range(0, len(self._gamestate.board()) - 1):
            for col in range(1, len(self._gamestate.board()[0])):
                self._draw_white_jewel(row, col)
        pygame.display.flip()

    def _draw_board(self) -> None:
        'Draws the board'
        for row in range(0, len(self._gamestate.board()) - 1):
            for col in range(1, len(self._gamestate.board()[0])):
                self._draw_color_jewel(row, col)

    def _draw_next_faller(self) -> None:
        'Draws the upcoming faller next to the board'
        pixel_width, pixel_height = self._get_pixel_width_and_height()
        
        for count in range(3):
            self._draw_faller_cell(count)

        self._next_faller_image_scaled = pygame.transform.scale(self._next_faller_image, (NEXT_FALLER_IMAGE_FRAC_WIDTH * pixel_width, NEXT_FALLER_IMAGE_FRAC_HEIGHT*pixel_height))
        self._surface.blit(self._next_faller_image_scaled, (NEXT_FALLER_TITLE_FRAC_X * pixel_width, NEXT_FALLER_TITLE_FRAC_Y * pixel_height))

    def _draw_faller_cell(self, count) -> None:
        'Draws a cell of a faller'
        _cell_color = self._get_cell_color(self._next_faller.jewel()[count])
        self._draw_next_faller_jewel(_cell_color, count)

    def _draw_color_jewel(self, row, col) -> None:
        'Draws a jewel with its color, or with the background color if the cell has no jewel'
        _cell_color = self._get_cell_color(self._gamestate.board()[row][col])
        if _cell_color == None:
            _cell_color = pygame.Color(BG_COLOR)

        self._draw_jewel(_cell_color, row, col)


    def _draw_white_jewel(self, row, col) -> None:
        'Draws a jewel as white if it is matching'
        _cell_color = self._get_cell_color(self._gamestate.board()[row][col])
        if self._is_cell_matched(row, col) == True:
            _cell_color = pygame.Color(WHITE)
            self._score += 1
        if self._get_cell_color(self._gamestate.board()[row][col]) == None:
            _cell_color = pygame.Color(BG_COLOR)
        
        self._draw_jewel(_cell_color, row, col)

    def _draw_next_faller_jewel(self, _cell_color, count):
        'Draws a cell of the next faller'
        pixel_width, pixel_height = self._get_pixel_width_and_height()

        fracx_tl = NEXT_FALLER_FRAC_X
        fracy_tl = NEXT_FALLER_FRAC_Y + JEWEL_FRAC_HEIGHT*count

        pixelx_tl = fracx_tl * pixel_width
        pixely_tl = fracy_tl * pixel_height
        rect_pixel_width = JEWEL_FRAC_WIDTH * pixel_width
        rect_pixel_height = JEWEL_FRAC_HEIGHT * pixel_height

        pygame.draw.ellipse(self._surface, _cell_color, (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height))
        pygame.draw.ellipse(self._surface, pygame.Color(WHITE), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 6)
        pygame.draw.ellipse(self._surface, pygame.Color(BG_COLOR), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 2)

    def _draw_jewel(self, _cell_color, row, col) -> None:
        'Handles the drawing of each cell'
        pixel_width, pixel_height = self._get_pixel_width_and_height()
        
        fracx_tl = JEWEL_FRAC_X + JEWEL_FRAC_WIDTH*(col-1)
        fracy_tl = JEWEL_FRAC_Y + JEWEL_FRAC_HEIGHT*row

        pixelx_tl = fracx_tl * pixel_width
        pixely_tl = fracy_tl * pixel_height
        rect_pixel_width = JEWEL_FRAC_WIDTH * pixel_width
        rect_pixel_height = JEWEL_FRAC_HEIGHT * pixel_height

        if self._is_cell_faller(row, col) == True:
            pygame.draw.ellipse(self._surface, _cell_color, (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height))
            pygame.draw.ellipse(self._surface, pygame.Color(WHITE), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 6)
            pygame.draw.ellipse(self._surface, pygame.Color(BG_COLOR), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 2)
            
        elif self._is_cell_landed(row, col) == True:
            pygame.draw.rect(self._surface, _cell_color, (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), border_radius = 20)
            pygame.draw.rect(self._surface, pygame.Color(WHITE), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 6, border_radius = 20)
            pygame.draw.rect(self._surface, pygame.Color(BG_COLOR), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 2, border_radius = 20)
            
        else:
            pygame.draw.rect(self._surface, _cell_color, (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), border_radius = 20)
            pygame.draw.rect(self._surface, pygame.Color(JEWEL_OUTLINE), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 6, border_radius = 20)
            pygame.draw.rect(self._surface, pygame.Color(BG_COLOR), (pixelx_tl, pixely_tl, rect_pixel_width, rect_pixel_height), width = 2, border_radius = 20)


    def _get_cell_color(self, cell: str) -> pygame.Color:
        'Returns the color of the jewel that a specific cell contains; returns the background color otherwise'
        _jewel = list(cell)[1].upper()
        if _jewel == 'S':
            return pygame.Color(S_COLOR)
        elif _jewel == 'T':
            return pygame.Color(T_COLOR)
        elif _jewel == 'V':
            return pygame.Color(V_COLOR)
        elif _jewel == 'W':
            return pygame.Color(W_COLOR)
        elif _jewel == 'X':
            return pygame.Color(X_COLOR)
        elif _jewel == 'Y':
            return pygame.Color(Y_COLOR)
        elif _jewel == 'Z':
            return pygame.Color(Z_COLOR)
        else:
            None

    def _get_pixel_width_and_height(self) -> tuple[int, int]:
        'Returns width and height of surface'
        return self._surface.get_width(), self._surface.get_height()

    def _is_cell_matched(self, row: int, col: int) -> bool:
        'Returns true if a cell contains a jewel that is part of a match; false otherwise'
        if '*' in self._gamestate.board()[row][col]:
            return True
        return False

    def _is_cell_faller(self, row: int, col: int) -> bool:
        'Returns true if a cell contains a faller that has no landed yet; false otherwise'
        if '[' in self._gamestate.board()[row][col]:
            return True
        return False

    def _is_cell_landed(self, row: int, col: int) -> bool:
        'Returns true if a cell contains a faller that has landed; false otherwise'
        if '|' in self._gamestate.board()[row][col]:
            return True
        return False

    def _end_game(self) -> None:
        'Sets the running attribute to false'
        self._running = False


    def _resize_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

if __name__ == '__main__':
    columns_game().run()
