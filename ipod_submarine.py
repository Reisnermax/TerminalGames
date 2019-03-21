#!/usr/bin/env
import sys
import threading
import socket
import numpy
import curses
import random
import time

############### GLOBAL VARIABLES ###############

key_queue = []
height = 0
width = 0
random_questions = True
host_ip = ""

############### THREADING FUNCTIONS ###############



def key_parser(stdscr):
    while True:
        key_queue.append(stdscr.getch())

def draw(stdscr):
    while True:
        stdscr.clear()
        if len(key_queue) != 0:
            stdscr.addstr(0,0, str(key_queue[len(key_queue)-1]))
        stdscr.refresh()



############### HELPFUL FUNCTIONS ###############



def place_middle(stdscr, y, str, atr=0):
    stdscr.addstr(y, (width-len(str))/2, str, atr)

def place_toggle_option(stdscr, y, str, bool, atr=0):
    str_begin = ((width-len(str))/2)-4
    stdscr.addstr(y, str_begin, str, atr)
    if bool:
        stdscr.addstr(y, str_begin + len(str) + 2, "  ", curses.color_pair(1))
    else:
        stdscr.addstr(y, str_begin + len(str) + 2, "  ", curses.color_pair(2))

def place_blanks(stdscr, y, str, full_str, atr=0):
    str_begin = ((width-len(full_str))/2)
    paste_str = str + full_str[len(str):]
    stdscr.addstr(y, str_begin, paste_str, atr)

def check_upkey(key):
    if key == 259 or key == 119:
        return True

def check_downkey(key):
    if key == 258 or key == 115:
        return True

def check_enter(key):
    if key == 10 or key == 32:
        return True

def standard_keycheck(key):
    if check_upkey(key):
        return -1
    elif check_downkey(key):
        return 1
    else:
        return 0

def limit_selection(max, min, select):
    if select > max:
        return max
    elif select < min:
        return min
    else:
        return select



############### MENU FUNCTIONS ###############

def host_game(stdscr):
    raise Exception("Not there yet...")

def client_game(stdscr):
    raise Exception("Getting there... The ip you entered: " + host_ip)

def ip_menu(stdscr):
    selection = 0
    global host_ip
    input_ip = ""

    while True:
        pass
        stdscr.clear()
        if len(key_queue) != 0:
            if key_queue[0] == 127:
                if len(input_ip) != 0:
                    if input_ip[len(input_ip)-1] == ".":
                        input_ip = input_ip[:len(input_ip)-2]
                    else:
                        input_ip = input_ip[:len(input_ip)-1]
            elif key_queue[0] < 255:
                if (chr(key_queue[0])).isdigit():
                    if (len(input_ip)+1) % 4 == 0 and len(input_ip) != 0:
                        input_ip = input_ip + "."
                    input_ip = input_ip + chr(key_queue[0])
                    if len(input_ip) > 15:
                        input_ip = input_ip[:15]
            selection = selection + standard_keycheck(key_queue[0])
            if check_enter(key_queue[0]):
                del key_queue[0]
                break
            del key_queue[0]
            election = limit_selection(1, 0, selection)
        place_middle(stdscr, 7, "Host IP:")
        if selection == 0:
            place_blanks(stdscr, 10, input_ip, "---.---.---.---", curses.A_BLINK)
            place_middle(stdscr, 12, "Back")
        elif selection == 1:
            place_blanks(stdscr, 10, input_ip, "---.---.---.---")
            place_middle(stdscr, 12, "Back", curses.A_BLINK)
        stdscr.refresh()

    if selection == 0:
        host_ip = input_ip
        client_game(stdscr)
    elif selection == 1:
        main_menu(stdscr)

def help_menu(stdscr):
    global random_questions
    selection = 0
    while True:
        pass
        stdscr.clear()
        if len(key_queue) != 0:
            selection = selection + standard_keycheck(key_queue[0])
            if check_enter(key_queue[0]):
                del key_queue[0]
                break
            del key_queue[0]
            selection = limit_selection(1, 0, selection)
        if selection == 0:
            place_middle(stdscr, 7, "Help and Options")
            place_toggle_option(stdscr, 10, "Random Questions", random_questions, curses.A_BLINK)
            place_middle(stdscr, 12, "Main Menu")
        elif selection == 1:
            place_middle(stdscr, 7, "Help and Options")
            place_toggle_option(stdscr, 10, "Random Questions", random_questions)
            place_middle(stdscr, 12, "Main Menu", curses.A_BLINK)
        stdscr.refresh()

    if selection == 0:
        random_questions = not random_questions
        help_menu(stdscr)
    elif selection == 1:
        main_menu(stdscr)



def main_menu(stdscr):
    selection = 0

    while True:
        stdscr.clear()
        if len(key_queue) != 0:
            selection = selection + standard_keycheck(key_queue[0])
            if check_enter(key_queue[0]):
                del key_queue[0]
                break
            del key_queue[0]
            selection = limit_selection(3, 0, selection)

        if selection == 0:
            place_middle(stdscr, 7, "Elon Musk's Ipod Submarine")
            place_middle(stdscr, 10, "Join Game", curses.A_BLINK)
            place_middle(stdscr, 12, "Host Game")
            place_middle(stdscr, 14, "Help/Options")
            place_middle(stdscr, 16, "Exit")
        elif selection == 1:
            place_middle(stdscr, 7, "Elon Musk's Ipod Submarine")
            place_middle(stdscr, 10, "Join Game")
            place_middle(stdscr, 12, "Host Game", curses.A_BLINK)
            place_middle(stdscr, 14, "Help/Options")
            place_middle(stdscr, 16, "Exit")
        elif selection == 2:
            place_middle(stdscr, 7, "Elon Musk's Ipod Submarine")
            place_middle(stdscr, 10, "Join Game")
            place_middle(stdscr, 12, "Host Game")
            place_middle(stdscr, 14, "Help/Options", curses.A_BLINK)
            place_middle(stdscr, 16, "Exit")
        elif selection == 3:
            place_middle(stdscr, 7, "Elon Musk's Ipod Submarine")
            place_middle(stdscr, 10, "Join Game")
            place_middle(stdscr, 12, "Host Game")
            place_middle(stdscr, 14, "Help/Options")
            place_middle(stdscr, 16, "Exit", curses.A_BLINK)

        stdscr.refresh()

    if selection == 0:
        ip_menu(stdscr)
    elif selection == 1:
        pass
        host_game(stdscr)
    elif selection == 2:
        help_menu(stdscr)
    elif selection == 3:
        sys.exit()



def main(stdscr):
    global height, width
    height, width = stdscr.getmaxyx()

    key_thread = threading.Thread(name='key_parser', target=key_parser, args=(stdscr,))
    key_thread.setDaemon(True)
    key_thread.start()

    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

    #draw(stdscr)
    main_menu(stdscr)

############### START ###############

if __name__ == "__main__":
    curses.wrapper(main)
