#############################################################
# FILE   : boggle.py
# WRITER : OREN EYAL, oreneyal15
# WRITER : DANIEL TAL, danieltal
# EXERCISE : intro2cs1 ex12 2021
#############################################################
import tkinter as tk
from tkinter import messagebox
from boggle_game_logic import *

LABEL_STYLE = {"font": ("Noto Sans CJK SC", 20), "width": 30, "height": 2,
               "bg": "white", "anchor": "w"}
BUTTON_STYLE = {"activebackground": "white", "activeforeground": "blue",
                "width": 4, "height": 3, "font": ("Noto Sans CJK SC", 15),
                "bg": "bisque2"}

END_MESSAGE = ("game over", "Do yo want to play again?")


class BoggleGui:
    """ this class responsible for the graphics of the game """
    _buttons_dic = {}

    def __init__(self, game):
        """This function initializes the boggle window"""
        self.__game = game
        root = tk.Tk()
        root.geometry("700x650")
        root.resizable(False, False)
        root.title("Boggle")
        self.__game_time = self.__game.get_time()
        self.__main_window = root
        self.frame_and_buttons()
        self.label_and_box()
        self.set_display()
        self._create_buttons()
        self.pack()

    def frame_and_buttons(self):
        """This function creates the frames of the window and the submit
        button"""
        self.__outer_frame = tk.Frame(self.__main_window, width=20, height=30,
                                      bg="white")

        self._lower_frame = tk.Frame(self.__main_window, bg="white", width=20,
                                     height=20)

        self.__low_frame = tk.Frame(self.__main_window, width=20, height=30)

        self.__words_frame = tk.Frame(self.__main_window, width=25, height=1,
                                      bg="white")

        self.__submit_button = tk.Button(self.__low_frame, text="start",
                                         command=self.press_start, width=20,
                                         height=4,
                                         font=("Noto Sans CJK SC", 15),
                                         bg="turquoise")

    def label_and_box(self):
        """this function creates the display labels and title box of the
        game"""
        self.__title_box = tk.Label(self.__words_frame, text="words list",
                                    font=("segoe print", 20), width=15,
                                    bg="cyan")
        self.__time_display = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__score_display = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__word_display = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__lst_box = tk.Listbox(self.__words_frame, background="orange",
                                    font=("Noto Sans CJK SC", 12), width=10,
                                    height=20)

    def pack(self):
        """This function packs the labels, frames and submit button in to
            the game window"""
        self.__time_display.pack(side=tk.TOP)
        self.__score_display.pack(side=tk.TOP)
        self.__word_display.pack(side=tk.TOP)
        self.__title_box.pack(side=tk.TOP)
        self.__lst_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.__words_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.__outer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._lower_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.__low_frame.pack(side=tk.BOTTOM, expand=True)
        self.__submit_button.pack()

    def set_display(self, word="", score=0):
        """This function sets the start screen display"""
        self.__word_display["text"] = "word: " + word
        self.__score_display["text"] = "score: " + str(score)
        display = "time: {:2d}:{:02d}".format(self.__game_time // 60,
                                              self.__game_time % 60)
        self.__time_display["text"] = display

    def _create_buttons(self):
        """This function creates a grid for the buttons of the game"""
        for i in range(self.__game.get_length()):
            tk.Grid.columnconfigure(self._lower_frame, i, weight=1)
        for i in range(self.__game.get_length()):
            tk.Grid.rowconfigure(self._lower_frame, i, weight=1)

    def _make_button(self, rowspan=1, columnspan=1):
        """This function creates the buttons of letters of the game"""
        for i in range(self.__game.get_length()):
            for j in range(self.__game.get_length()):
                button_char = self.__game.get_letter(i, j)
                word_tup = (i, j, button_char + str(i) + str(j))
                button = tk.Button(self._lower_frame, text=button_char,
                                   **BUTTON_STYLE, command=lambda x=word_tup:
                    self.letter_press(*x))
                button.grid(row=i, column=j, rowspan=rowspan,
                            columnspan=columnspan, sticky=tk.NSEW)
                self._buttons_dic[button_char + str(i) + str(j)] = button

    def letter_press(self, row, col, word_tup):
        """This function updates the word in display after a letter
            was clicked"""
        if self.__game.update_word(row, col):
            button = self._buttons_dic[word_tup]
            button["bg"] = "chocolate1"
        self.__word_display["text"] = "word: " + self.__game.get_word_display()

    def press_submit(self):
        """This function checks if the current word is correct after the user
           pressed submit"""
        for i in self._buttons_dic:
            self._buttons_dic[i]["bg"] = "bisque2"

        word = self.__game.get_word_display()
        if self.__game.check_word():
            self.__score_display["text"] = "score: " + str(
                self.__game.get_score())
            self.__lst_box.insert("end", word)
        self.__word_display["text"] = "word: "

    def press_start(self):
        """This function is the command of the start button"""
        self.__game.reset_word_and_path()
        self.__word_display["text"] = "word: "
        self.__submit_button["text"] = "submit"
        self.__submit_button["command"] = self.press_submit
        self._make_button()
        self.timer()

    def timer(self):
        """This function moves the timer of the game"""
        minutes = self.__game_time // 60
        seconds = self.__game_time % 60
        self.__time_display["text"] = "time: {:2d}:{:02d}".format(minutes,
                                                                  seconds)
        if self.__game_time != 0:
            self.__game_time -= 1
            self.__main_window.after(1000, self.timer)
        else:
            self.__time_display["text"] = "TIMES UP!"
            self.end_game()

    def end_game(self):
        """This function maneges if the user wants to play again"""
        result = messagebox.askquestion(*END_MESSAGE, icon="question")
        if result == "yes":
            self.play_again()
        else:
            self.__main_window.destroy()

    def play_again(self):
        """This function restarts a new game"""
        for i in self._buttons_dic:
            self._buttons_dic[i]["bg"] = "bisque2"
        self.__game.reset_game()
        self.__game_time = self.__game.get_time()
        self.set_display()
        self.__submit_button.config(text="start", command=self.press_start)
        self.__lst_box.delete(0, "end")

    def run(self):
        """This function runs the game loop"""
        self.__main_window.mainloop()


if __name__ == '__main__':
    game = Game("boggle_dict.txt")
    game1 = BoggleGui(game)
    game1.run()
