#############################################################
# FILE   : ex12_utils.py
# WRITER : OREN EYAL, oreneyal15
# WRITER : DANIEL TAL, danieltal
# EXERCISE : intro2cs1 ex12 2021
#############################################################
import itertools


def load_words_dict(file_path):
    """ This function loads the list of words """

    word_dict = {}
    with open(file_path, 'r') as words:
        word = words.read().splitlines()
        for i in word:
            word_dict[i] = True
    return word_dict


def is_valid_path(board, path, words):
    """ This function checks if a particular route is correct
     and if so returns a word """

    if not path:
        return
    word = ""
    for i in range(len(path) - 1):
        if abs(path[i][0] - path[i + 1][0]) != 1 and abs(
                path[i][0] - path[i + 1][0]) != 0:
            return
        if abs(path[i][1] - path[i + 1][1]) != 1 and abs(
                path[i][1] - path[i + 1][1]) != 0:
            return
        if path[i][0] == path[i + 1][0] and path[i][1] == path[i + 1][1]:
            return
        if path[i][0] >= len(board) or path[i][1] >= len(board):
            return
        word += board[path[i][0]][path[i][1]]
    if path[-1][0] >= len(board) or path[-1][1] >= len(board):
        return
    word += board[path[-1][0]][path[-1][1]]
    if word in words:
        return word
    else:
        return


def find_length_n_words(n, board, words):
    """This function returns all the correct n-length words on the board"""
    cell_list = [(i, j) for i in range(4) for j in range(4)]

    list_words = []
    for option in itertools.permutations(cell_list, n):
        word_tpl = check_word_in_path(board, list(option), n, words)

        if word_tpl is not None and word_tpl not in list_words:
            list_words.append(word_tpl)
    return list_words



def check_word_in_path(board, path, n, words):
    """helper function that tests a particular word"""
    path2 = []
    word = ""
    for location in path:
        word += board[location[0]][location[1]]
        path2.append(location)
        if len(word) == n:
            if check_path_validity(board, path2) and word in words:
                return (word, path2)
            else:
                return

def check_path_validity(board, path):
    """helper function that checks the integrity of a path """
    for i in range(len(path) - 1):
        if abs(path[i][0] - path[i + 1][0]) != 1 and abs(
                path[i][0] - path[i + 1][0]) != 0:
            return False
        if abs(path[i][1] - path[i + 1][1]) != 1 and abs(
                path[i][1] - path[i + 1][1]) != 0:
            return False
        if path[i][0] == path[i + 1][0] and path[i][1] == path[i + 1][1]:
            return False
        if path[i][0] >= len(board) or path[i][1] >= len(board):
            return False

    return True
