#columnsgame.py - The module that controls all of the logic and mechanics of the game.

from collections import namedtuple
import random

#   The below variables are set so that reading the code
#   is much more understandable.

GAME_OVER = False
EMPTY = '   '
FROZEN = 'FROZEN'
FALLING = 'FALLING'
VALID_JEWEL = 'STVWXYZ'


#   Below are a series of exceptions either cause the game to quit, because
#   the game may have reached an ending state, or give useful information
#   because they show that there has been an error of some sort, usually
#   in the case of invalid user input.

class GameOverError(Exception):
    GAME_OVER = True

class InvalidMoveError(Exception):
    pass

class FallerCantFitError(Exception):
    pass

class QuitEarlyError(Exception):
    pass

class InvalidFallerError(Exception):
    pass

class InvalidArgumentTypeError(Exception):
    pass

class NeitherContentsNorEmptyError(Exception):
    pass

class InvalidInputForRows(Exception):
    pass

class InvalidInputForColumns(Exception):
    pass


#   Below are two classes: the Faller class and the GameState class. The Faller
#   class creates and controls faller objects, such as by making them rotate or
#   move left or right. Objects of the GameState class make playable games that
#   contain useful information about the gamestate. And, the class contains methods
#   that allow the gamestate to be changed depending on the commands of the user.

class Faller:
    def __init__(self, faller: list):
        self._column = int(list(faller[0])[1])
        self._jewel = faller[1:]
        self._unfitted_jewel = []

    def reconnect_jewel(self) -> None:
        '''Reconnects the entire jewel by combining the jewel that
        currently fits on the board and the unfitted jewel'''
        
        self._jewel = self._unfitted_jewel + self._jewel
        self._unfitted_jewel.clear()

    def about_to_freeze(self) -> None:
        'Formats a jewel with vertical bars if it is about to freeze'
        for i in range(len(self._jewel)):
            self._jewel[i] = f'|{list(self._jewel[i])[1]}|'
        if self._unfitted_jewel != []:
            for i in range(len(self._unfitted_jewel)):
                self._unfitted_jewel[i] = f'|{list(self._unfitted_jewel[i])[1]}|'

    def no_longer_about_to_freeze(self) -> None:
        'Formats a jewel with square brackets if it is no longer about to freeze'
        for i in range(len(self._jewel)):
            self._jewel[i] = f'[{list(self._jewel[i])[1]}]'
        if self._unfitted_jewel != []:
            for i in range(len(self._unfitted_jewel)):
                self._unfitted_jewel[i] = f'[{list(self._unfitted_jewel[i])[1]}]'
    
    def column(self) -> int:
        return self._column

    def jewel(self) -> list:
        return self._jewel

    def unfitted_jewel(self) -> list:
        return self._unfitted_jewel

    def change_column(self) -> None:
        'Changes the current faller column to a random column between 1 and 6; inclusive'
        self._column = random.randrange(1,7)

    def remove_jewel(self, count: int) -> None:
        '''Removes parts of the jewel not on the board from
        the jewel attribute and instead places them in
        the unfitted_jewel attribute'''
        
        for i in range(len(self.jewel()) - count):
            self._unfitted_jewel.append(self._jewel[0]) 
            self._jewel.pop(0)
            
    
    def rotate(self) -> None:
        'Rotates the jewel'
        len_current_jewel = len(self._jewel)

        self.reconnect_jewel()
        
        len_entire_jewel = len(self._jewel)
        
        last_el = self._jewel[-1]
        for i in range(len(self._jewel) - 1, 0, -1):
            self._jewel[i] = self._jewel[i-1]
        self._jewel[0] = last_el

        
        self.remove_jewel(len_current_jewel)
        

    def move_right(self) -> None:
        'Adds 1 to the column number if faller moved right'
        self._column += 1

    def move_left(self) -> None:
        'Subtracts 1 from the column number if the faller moved left'
        self._column -= 1

    def update_jewel(self) -> None:
        '''In the special case that a frozen jewel freezes
        and matches while there is are still parts of the jewel
        not shown on the board, updates jewel so that it now
        contains the unfitted parts'''
        
        self._jewel = self._unfitted_jewel[:]
        self._unfitted_jewel.clear()


class GameState:
    def __init__(self, board: list[list], faller: Faller, count: int, state: str):
        self._board = board
        self._faller = faller
        self._count = count
        self._state = state
        self._matching = True
        self._check_input()

    def _check_input(self) -> None:
        '''Makes sure that the arguments passed while trying to
        initialize a GameState object are of valid types'''
        
        if type(self._board) is list \
        and type(self._faller) is type(None) or type(Faller) \
        and type(self._count) is int \
        and type(self._state) is str \
        and type(self._matching) is bool:
            pass
        else:
            raise InvalidArgumentTypeError()

    def columns(self) -> int:
        'Returns the number of playable columns'
        return len(self._board[0]) - 2

    def rows(self) -> int:
        'Returns the number of playabale rows'
        return len(self._board) - 1

    def board(self):
        return self._board

    def faller(self):
        return self._faller

    def count(self):
        return self._count

    def state(self):
        return self._state

    def matching(self):
        return self._matching

    def tick_count(self) -> None:
        'Increases the count by 1'
        self._count += 1

    def update_matching(self, true_or_false: bool) -> None:
        self._matching = true_or_false

    def update_faller(self, faller: Faller) -> None:
        self._faller = faller

    def update_board(self, board: list[list]) -> None:
        self._board = board

    def update_state(self, state) -> None:
        self._state = state

    def update_count(self, count) -> None:
        self._count = count

    def check_game__over(self) -> None:
        'Checks if a game is over when a faller freezes'
        if type(self._faller) is not type(None):
            if self._faller.unfitted_jewel() != []:
                raise GameOverError
            else:
                pass

    def edit_board__post_moving_faller(self, count: int) -> None:
        '''Updates the board of the game if a
        faller is moved left or right'''
        
        board = self.board()[:]
        
        if self.count() == get_bottom_row(self.faller().column(), self):
            self.faller().remove_jewel(count)
            if count < len(self.faller().jewel()):
                for row in range(count):
                    board[row][self.faller().column()] = f'|{board[row][self.faller().column()][1]}|'
            else:
                for row in range(count - len(self.faller().jewel()), count):
                    board[row][self.faller().column()] = f'|{board[row][self.faller().column()][1]}|'
                    
        else:
            if count < len(self.faller().jewel()):
                for row in range(count):
                    board[row][self.faller().column()] = f'[{board[row][self.faller().column()][1]}]'
                    self.faller().reconnect_jewel()
            else:
                for row in range(count - len(self.faller().jewel()), count):
                    board[row][self.faller().column()] = f'[{board[row][self.faller().column()][1]}]'
                    self.faller().reconnect_jewel()
                    
        self.update_board(board)
        
    def move_faller_left(self) -> None:
        'Moves the faller left'
        board = self.board()[:]
        column_index = self.faller().column()
        
        if column_index == 1:
            pass
        
        else:
            for i in range(len(self.board()) - 1, -1, -1):
                if is_cell__faller(self.board()[i][column_index]) == True: 
                    if check_left_cell__is_empty(self, i) == True: 
                        board = move_cell_left__empty_current_cell(self, i)
                    else:
                        raise InvalidMoveError()
            self.faller().move_left()
            
        self.update_board(board)

    def move_faller_right(self) -> None:
        'Moves the faller right'
        board = self.board()[:]
        column_index = self.faller().column()

        if column_index == len(self.board()[0]) - 2:
            pass
        
        else:
            for i in range(len(self.board()) - 1, -1, -1):
                if is_cell__faller(self.board()[i][column_index]) == True:
                    if check_right_cell__is_empty(self, i) == True: 
                        board = move_cell_right__empty_current_cell(self, i)
                    else: 
                        raise InvalidMoveError()
            self.faller().move_right()
            
        self.update_board(board)

 
    def drop_all_cells_once(self) -> None:
        'Drops a cell if there is an empty space below'
        board = self.board()[:]
        for i in range(len(board) - 1):
            for j in range(1, len(board[0])):
                if board[i + 1][j] == EMPTY:
                    board[i + 1][j] = board[i][j]
                    board[i][j] = EMPTY
        self.update_board(board)

    def starting_unique_field__all_cells_fall(self) -> None:
        'Updates a starting board if there are empty spaces'
        board = gamestate.board()[:]
        for i in range(len(board) - 1):
            for j in range(1, len(board[0]) - 1):
                if is_below__empty(gamestate, i, j) is True:
                    board[i + 1][j] = board[i][j]
                    board[i][j] = EMPTY
        gamestate.update_board(board)
        
    def handle_command(self, user_command) -> None:
        '''This is the main method that changes the GameState object depending
        on the input of the user. The user may make a Faller, pass time, move
        the faller left or right, quit the game, or rotate the faller'''
        
        
        if not input__passage_of_time(user_command):
            user_command = list(user_command)
            
            if self.state() == FROZEN:
                if input__make_faller(user_command) is True:
                    faller = make_faller(_raw_command, self)
                    self.update_state(FALLING)
                    self.update_count(0)
                    self.update_faller(faller)
                    if is_below__empty(self, -1, faller.column()) is False:
                        print('GAME OVER')
                        raise FallerCantFitError()
                    self.drop_faller()
                    
            elif self.state() == FALLING:
                if input__rotate_jewel(user_command) is True:
                    self.faller().rotate()
                    self.update_board(update_board__rotated_faller(self))

                elif input__move_faller_left(user_command) is True:
                    try:
                        self.move_faller_left()
                        self.faller().no_longer_about_to_freeze()
                        self.edit_board__post_moving_faller(self.count())
                    except InvalidMoveError:
                        pass
                    
                elif input__move_faller_right(user_command) is True:
                    try:
                        self.move_faller_right()
                        self.faller().no_longer_about_to_freeze()
                        self.edit_board__post_moving_faller(self.count())
                    except InvalidMoveError:
                        pass
                
            if input__quit_game(user_command) is True:
                raise QuitEarlyError()

            else:
                pass
                
        else:
            if self.state() != FROZEN:
                self.drop_faller()
                if is_matching_possible(self) is False and self.state() == FROZEN:
                    self.check_game__over()

                if self.count() == 0:
                    self.update_board(update_board__possible_matches(self))
                    for i in range(len(self.board()) - 2):
                        self.drop_all_cells_once()
                
            elif self.state() == FROZEN:
                self.update_board(update_board__possible_matches(self))
                for i in range(len(self.board()) - 2):
                    self.drop_all_cells_once()
                self.update_board(match_jewels(self))
            
                if self.faller() != None:
                    if self.faller().unfitted_jewel() != [] and is_below__empty(self, -1, self.faller().column()) is True:
                        self.update_count(0)
                        self.update_state(FALLING)
                        self.faller().update_jewel()
                        self.faller().no_longer_about_to_freeze()
                        self.drop_faller()
                self.check_game__over()
                
    def drop_faller(self) -> None:
        '''This method controls the act of dropping a faller
        using the count attribute as a central mechanic. Depending on
        the count of the game, this method chooses what should happen
        to the faller if the user chooses time to pass'''
        
        _faller_column = self.faller().column()
        _jewel = self.faller().jewel()
        board = self.board()[:]

        if self.count() == 0 and is_below__empty(self, -1, _faller_column) is False:
            print('GAME OVER')
            raise GameOverError()

        if self.count() == 0 and get_bottom_row(_faller_column, self) != 0:
            board[self.count()][_faller_column] = _jewel[-1]
            
            if self.count() == get_bottom_row(_faller_column, self) - 1:
                self.faller().about_to_freeze()
                self.faller().remove_jewel(self.count() + 1)
                board[self.count()][_faller_column] = f'|{list(self.board()[0][_faller_column])[1]}|'
                
        elif self.count() < len(_jewel): 
            for i in range(self.count() - 1, -1, -1):
                board[i + 1][_faller_column] = self.board()[i][_faller_column]
            board[0][_faller_column] = _jewel[-1*self.count() - 1]
            
            if self.count() == get_bottom_row(_faller_column, self) - 1:
                if can_faller_fall(self) == True or can_entire_faller_fit(self) == True:
                    for i in range(self.count(), self.count() - len(_jewel), -1):
                        self.faller().about_to_freeze()
                        board[i][_faller_column] = f'|{list(self.board()[i][_faller_column])[1]}|'
                        
                else:
                    self.faller().about_to_freeze()
                    self.faller().remove_jewel(self.count() + 1)
                    for i in range(self.count(), self.count() - len(_jewel), -1):
                        board[i][_faller_column] = f'|{list(self.board()[i][_faller_column])[1]}|'

                        
        elif self.count() <= get_bottom_row(_faller_column, self) - 1:
            for i in range(self.count() - 1, -1, -1):
                board[i + 1][_faller_column] = self.board()[i][_faller_column]
                
            for i in range(self.count() - len(_jewel), -1, -1):
                board[i][_faller_column] = EMPTY
                
            if self.count() == get_bottom_row(_faller_column, self) - 1:
                for i in range(self.count(), self.count() - len(_jewel), -1):
                    self.faller().about_to_freeze()
                    board[i][_faller_column] = f'|{list(self.board()[i][_faller_column])[1]}|'
                    
        else:
            for i in range(self.count() - 1, self.count() - len(_jewel) - 1, -1):
                board[i][_faller_column] = f' {list(self.board()[i][_faller_column])[1]} '
            self.update_matching(True)
            self.update_board(match_jewels(self))
            self.update_state(FROZEN)
            self.tick_count()
                                    
        self.update_board(board)
        self.tick_count()

    def print_field(self) -> None:
        'Prints the board'
        for i in self._board:
            for j in range(len(i)):
                print(i[j], end = '')

    def make_random_faller(self) -> Faller:
        'Creates a faller with a random column and random set of jewels'
        _faller = [f'[{self.get_random_column()}]']
        for i in range(0,3):
            _faller.append(f'[{self.random_jewel()}]')
        return Faller(_faller)

    def random_jewel(self) -> str:
        'Returns a random jewel'
        jewel_key = random.randrange(0,7)
        return key_to_jewel(jewel_key)

    def check_if_board_is_full(self) -> bool:
        'Returns False if entire board is full; true otherwise'
        for i in range(1, len(self.board()[0]) - 1):
            if get_bottom_row(i, self) > 0:
                return True
            else:
                pass
        return False

    def get_random_column(self) -> int:
        'Returns a random column, making sure that it is not one that is already completely filled; if not possible, raises GameOverError'
        if self.check_if_board_is_full() == True:   
            col = random.randrange(1,7)
            if get_bottom_row(col, self) > 0:
                return col
            else:
                return self.get_random_column()
        else:
            raise GameOverError()



#   These methods are independent of the above classes and perform
#   a very diverse set of functions.
         
def ask_and_get_rows() -> int:
    'Asks for the number of rows'
    try:
        rows = int(input())
        return rows
    except:
        raise InvalidInputForRows()

def ask_and_get_columns() -> int:
    'Asks for the number of columns'
    try:
        columns = int(input())
        return columns
    except:
        raise InvalidInputForColumns()

def state_of_starting_field() -> str:
    '''Detrmines whether or not the user chose to have an empty starting field
    or a starting field with specified contents'''
    empty_or_contents = input().upper()
    return empty_or_contents

def _get_contents_of_unempty_starting_field(number_of_rows: int, number_of_columns: int) -> list[list[int]]:
    'Creates a board with starting contents'
    starting_field = []
    for i in range(0,number_of_rows):
        row = list(input().upper())
        starting_field.append(row)
    return starting_field

def is_game_over() -> bool:
    'Checks if game is over'
    return GAME_OVER

def update_board__possible_matches(gamestate) -> list[list[int]]:
    'Iterates through a board and removes any matched jewels'
    board = gamestate.board()[:]
    for i in range(len(board) - 2, -1, -1):
        for j in range(len(board[0]) - 1):
            if '*' in board[i][j]:
                board[i][j] = EMPTY
    return board

def update_board__rotated_faller(gamestate: GameState) -> list[list[int]]:
    'Returns an updated board after rotating faller'
    _copy_of_jewel = gamestate.faller().jewel()[:]
    board = gamestate.board()[:]
    for i in range(len(board) - 2, -1, -1):
        if '[' in board[i][gamestate.faller().column()]:
            board[i][gamestate.faller().column()] = _copy_of_jewel[-1]
            _copy_of_jewel.pop()  
        elif '|' in board[i][gamestate.faller().column()]:
            board[i][gamestate.faller().column()] = f'|{list(_copy_of_jewel[-1])[1]}|'
            _copy_of_jewel.pop()
    return board
                  
def can_faller_fall(gamestate: GameState) -> bool:
    'Returns true if a faller can fall down a cell'
    if gamestate.count() >= get_bottom_row(gamestate.faller().column(), gamestate) - 1:
        return False
    return True

def can_entire_faller_fit(gamestate: GameState) -> bool:
    '''Returns true if the len of the current faller is less or equal to the amount of empty spaces
    in the specific column that the faller is falling in'''
    if len(gamestate.faller().jewel()) >= get_bottom_row(gamestate.faller().column(), gamestate) + 1:
        return False
    return True

def make_faller(raw_command: str, game: GameState) -> Faller:
    'Creates a new Faller object'
    _faller = []
    _raw_command = list(raw_command)[2:]
    if is_faller_valid(_raw_command, game) is True:
        for i in range(4):
            _faller.append(f'[{_raw_command[2*i]}]')
        return Faller(_faller)
    else:
        raise InvalidFallerError()



def key_to_jewel(key: int) -> str:
    'Assigns each jewel to a unique number'
    if key == 0:
        return 'S'
    elif key == 1:
        return 'T'
    elif key == 2:
        return 'V'
    elif key == 3:
        return 'W'
    elif key == 4:
        return 'X'
    elif key == 5:
        return 'Y'
    elif key == 6:
        return 'Z'

def is_faller_valid(raw_command: str, gamestate: GameState) -> bool:
    '''Determines whether or not the user followed correct formatting, chose valid
    jewels, and chose a playable column when creating a faller'''
    try:
        _column = int(raw_command[0])
        _first_jewel = raw_command[2]
        _second_jewel = raw_command[4]
        _third_jewel = raw_command[6]
        _len_jewel = len(''.join(raw_command).strip())

        if 1 <= _column <= gamestate.columns() \
        and _first_jewel in VALID_JEWEL \
        and _second_jewel in VALID_JEWEL \
        and _third_jewel in VALID_JEWEL \
        and _len_jewel == 7:
            return True
        return False
    except:
        return False


def get_bottom_row(column: int, gamestate: GameState) -> int:
    '''Returns the index of the lowest column,
    0 meaning that the entire column is filled'''
    for i in range(len(gamestate.board())):
        if gamestate.board()[i][column] == EMPTY or '[' in gamestate.board()[i][column]:
            pass
        elif '|' in gamestate.board()[i][column]:
            pass
        else:
            return i
    return -1

def starting_gamestate(num_of_rows: int, num_of_columns: int) -> GameState:
    'Returns a GameState object with the starting board'
    user_input = input().strip()
    if user_input == 'EMPTY':
        return GameState(make_empty_field(num_of_rows, num_of_columns), None, 0, FROZEN)
    elif user_input == 'CONTENTS': 
        gamestate = GameState(make_unique_field(num_of_rows, num_of_columns), None, 0, FROZEN)
        for i in range(len(gamestate.board())):
            gamestate.drop_all_cells_once()
        return GameState(match_jewels(gamestate), None, 0, FROZEN)
    else:
        raise NeitherContentsNorEmptyError()

def make_unique_field(num_of_rows: int, num_of_columns: int) -> list[list]:
    'Creates a unique field given specified jewels'
    rows = []
    field = []
    for i in range(num_of_rows):
        _input = list(input())
        if not _input:
            rows.append([' '] * num_of_columns)
        else:
            rows.append(_input)
    for i in range(num_of_rows):
        row = ['|']
        for j in range(len(rows[i])):
            row.append(f' {rows[i][j]} ')
        row.append('|\n')
        field.append(row)
    row = [' ']
    for i in range(len(rows)):
        row.append('---')
    row.append(' ')
    field.append(row)
    return field

def make_empty_field(number_of_rows: int, number_of_columns: int) -> list[list]:
    'Creates an empty board'
    field = []
    for i in range(number_of_rows):
        row = ['|']
        for j in range(number_of_columns):
            row.append('   ')
        row.append('|\n')
        field.append(row)
    row = [' ']
    for i in range(number_of_columns):
        row.append('---')
    row.append(' ')
    field.append(row)
    return field

def is_cell__faller(cell: str) -> bool:
    'Returns true if a cell is a part of a faller'
    if '[' in cell or '|' in cell:
        return True
    return False

def check_left_cell__is_empty(gamestate: GameState, row_index: int) -> bool:
    'Returns true if the left cell of a specific cell is empty'
    if gamestate.board()[row_index][gamestate.faller().column() - 1] == EMPTY:
        return True
    return False

def check_right_cell__is_empty(gamestate: GameState, row_index) -> bool:
    'Returns true if the right cell of a specific cell is empty'
    if gamestate.board()[row_index][gamestate.faller().column() + 1] == EMPTY:
        return True
    return False

def move_cell_left__empty_current_cell(gamestate: GameState, row_index: int) -> list[list]:
    'Returns a board where a specific cell moved left'
    board = gamestate.board()
    board[row_index][gamestate.faller().column() - 1] = board[row_index][gamestate.faller().column()]
    board[row_index][gamestate.faller().column()] = '   '
    return board

def move_cell_right__empty_current_cell(gamestate: GameState, row_index: int) -> GameState:
    'Returns a board where a specific cell moved right'
    board = gamestate.board()
    board[row_index][gamestate.faller().column() + 1] = board[row_index][gamestate.faller().column()]
    board[row_index][gamestate.faller().column()] = EMPTY
    return board

def is_below__empty(gamestate: GameState, row: int, column: int) -> bool:
    'Returns true if a cell has empty space beneath it'
    if gamestate.board()[row + 1][column] == EMPTY:
        return True
    return False




#   The below methods determine what the program should do
#   given a user command, because each input from the user will
#   cause exactly one of these to evaluate to true. The user can intend
#   to make a faller, pass time, move the faller left or right, rotate
#   the faller or quit the game.
    
def input__passage_of_time(user_command: str) -> bool:
    if not user_command:
        return True
    return False

def input__make_faller(user_command: list) -> bool:
    if user_command[0] == 'F':
        return True
    return False

def input__rotate_jewel(user_command: list) -> bool:
    if user_command[0] == 'R':
        return True
    return False

def input__move_faller_left(user_command: list) -> bool:
    if user_command[0] == '<':
        return True
    return False
    
def input__move_faller_right(user_command: list) -> bool:
    if user_command[0] == '>':
        return True
    return False

def input__quit_game(user_command: list) -> bool:
    if user_command[0] == 'Q':
        return True
    return False




#   The following methods control the matching aspect of the game,
#   including determining whether or not matching is possible,
#   updating the board so that matched jewels have astericks
#   around them, and updating the board after matched jewels
#   have been removed

def is_matching_possible(gamestate) -> bool:
    'Returns true if matching is possible'
    board = gamestate.board()[:]
    for row in range(len(board) - 1):
        for col in range(1, len(board[0]) - 1):
            if _three_or_more_in_a_row(board, row, col, 0, 1) \
            or _three_or_more_in_a_row(board, row, col, 1, 1)\
            or _three_or_more_in_a_row(board, row, col, 1, 0)\
            or _three_or_more_in_a_row(board, row, col, 1, -1)\
            or _three_or_more_in_a_row(board, row, col, 0, -1)\
            or _three_or_more_in_a_row(board, row, col, -1, -1)\
            or _three_or_more_in_a_row(board, row, col, -1, 0)\
            or _three_or_more_in_a_row(board, row, col, -1, 1) is True:
                return True
    return False

def match_jewels(gamestate: GameState) -> list[list[int]]:
    'Updates the GameState object so that its board includes all possible matchings'
    board = gamestate.board()[:]
    
    for row in range(len(gamestate.board()) - 1):
        for col in range(1, len(gamestate.board()[0]) - 1):
            gamestate.update_board(_matching_sequence_begins_at(board, row, col))

    return board
    


def _matching_sequence_begins_at(board: list[list[int]], row: int, col: int) -> list[list[int]]:
    '''Iterates through a board and if it finds a cell where matching begins,
    it returns a board with matching jewels, starting at the cell where the matching
    began. Since it is a series of if statements, matching can occur more than once
    before the board is returned'''
    
    if _three_or_more_in_a_row(board, row, col, 0, 1) is True:
        board = update_matching_board(board, row, col, 0, 1)
    if _three_or_more_in_a_row(board, row, col, 1, 1) is True:
        board = update_matching_board(board, row, col, 1, 1)
    if _three_or_more_in_a_row(board, row, col, 1, 0) is True:
        board = update_matching_board(board, row, col, 1, 0)
    if _three_or_more_in_a_row(board, row, col, 1, -1) is True:
        board = update_matching_board(board, row, col, 1, -1)
    if _three_or_more_in_a_row(board, row, col, 0, -1) is True:
        board = update_matching_board(board, row, col, 0, -1)
    if _three_or_more_in_a_row(board, row, col, -1, -1) is True:
        board = update_matching_board(board, row, col, -1, -1)
    if _three_or_more_in_a_row(board, row, col, -1, 0) is True:
        board = update_matching_board(board, row, col, -1, 0)
    if _three_or_more_in_a_row(board, row, col, -1, 1) is True:
        board = update_matching_board(board, row, col, -1, 1)
    return board
    

def update_matching_board(board: list[list[int]], row: int, col: int, coldelta: int, rowdelta: int) -> list[list[int]]:
    'For each match, updates the board so that it shows the matching jewels with astericks surrounding them'
    _copied_board = board[:]
    start_cell = list(board[row][col])[1]
    
    while list(board[row][col])[1] == start_cell:
        _copied_board[row][col] = f'*{list(board[row][col])[1]}*'
        col += coldelta
        row += rowdelta
        if len(board[row][col]) != 3: 
            return _copied_board

    return _copied_board
            
            

def _three_or_more_in_a_row(board: list[list[int]], row: int, col: int, coldelta: int, rowdelta: int) -> bool:
    '''Returns true if a specified cell is a starting cell where a
    match occurs containing three or more jewels'''
    start_cell = board[row][col]
    
    if start_cell == EMPTY:
        return False
        
    else:
        for i in range(1, 3):
            if not _is_valid_column_number(col + coldelta * i, board) \
                or not _is_valid_row_number(row + rowdelta * i, board) \
                or list(board[row + rowdelta * i][col + coldelta *i])[1] != list(start_cell)[1]:
                    return False
        return True
        
    
def _is_valid_column_number(column_number: int, board: list[list[int]]) -> bool:
    'Returns true if the given column number is valid'
    return 1 <= column_number < len(board[0])

def _is_valid_row_number(row_number: int, board: list[list[int]]) -> bool:
    'Returns True if the given row number is valid'
    return 0 <= row_number < len(board) - 1



