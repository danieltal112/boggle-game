#############################################################
# FILE   : boggle_game_logic.py
# WRITER : OREN EYAL, oreneyal15
# WRITER : DANIEL TAL, danieltal
# EXERCISE : intro2cs1 ex12 2021
#############################################################
import ex12_utils as ex12
import boggle_board_randomizer as board

GAME_TIME = 180


class Game:
    """ this class responsible for the rules of the game """

    def __init__(self, file_path, time=GAME_TIME):
        """The builder of the class game"""
        self.board = board.randomize_board()
        self.score = 0
        self.time = time
        self.chosen_words = []
        self.cur_word = ""
        self.cur_path = []
        self.words_dict = ex12.load_words_dict(file_path)

    def __add_score(self, length):
        """ add score to the player  """
        self.score = self.score + (length * length)

    def get_time(self):
        """returns the game time"""
        return self.time

    def get_score(self):
        """ return score  """
        return self.score

    def update_word(self, x, y):
        """This function adds a clicked letter to the word   """
        if (x, y) in self.cur_path:
            return False
        self.cur_path.append((x, y))
        if ex12.check_path_validity(self.board, self.cur_path):
            self.cur_word += self.board[x][y]
            return True
        else:
            self.cur_path.pop()
            return False

    def get_length(self):
        """this function returns the length of the board"""
        return len(self.board)

    def get_word_display(self):
        """this function returns the current word chosen fron the user   """
        return self.cur_word

    def get_letter(self, x, y):
        """This function returns a letter on the board by the coordinates
        received"""
        return self.board[x][y]

    def check_word(self):
        """this function checks if a word is valid and and if so updates the
        users score"""
        if self.cur_word is None:
            self.reset_word_and_path()
            return False
        if self.cur_word == ex12.is_valid_path(self.board, self.cur_path,
                                               self.words_dict):
            if self.cur_word not in self.chosen_words:
                self.chosen_words.append(self.cur_word)
                self.__add_score(len(self.cur_word))
                self.reset_word_and_path()
                return True
        self.reset_word_and_path()
        return False

    def reset_word_and_path(self):
        """This function resets the current word and word path after a word
        is submitted"""
        self.cur_word = ""
        self.cur_path = []

    def reset_game(self):
        """This function resets the game and creates a new board"""
        self.score = 0
        self.board = board.randomize_board()
