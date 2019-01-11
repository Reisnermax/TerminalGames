#!/usr/bin/env
import sys,os
import numpy
import curses
import random
import time

def draw(stdscr):

    direction = "right"
    k = 0
    cursor_x = 0
    cursor_y = 0
    color_counter = 0

    height, width = stdscr.getmaxyx()
    width = width // 2
    stdscr.clear()
    stdscr.refresh()

    snake_trail = []
    snake_length = 10

    pellet_coords = [random.randint(0,width-2), random.randint(0,height)]

    curses.start_color()

    trail_color = 1
    pellet_color = 2
    second_color = 3
    third_color = 4
    cursor_color = 5

    curses.init_pair(trail_color, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(pellet_color, curses.COLOR_MAGENTA, curses. COLOR_MAGENTA)
    curses.init_pair(second_color, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(third_color, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(cursor_color, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

    stdscr.nodelay(1)

    def regen_pellet():
        pellet_coords = [random.randint(0, (width//2) - 1), random.randint(0,height - 1)]
        stdscr.addstr(0,0,"SAFEWFASEFASFASDF")
        for snake_coords in snake_trail:
            if snake_coords == pellet_coords:
                regen_pellet()

    while k != ord('q'):

    	stdscr.clear()

        if k == curses.KEY_DOWN:
            if direction != "up":
                direction = "down"
        elif k == curses.KEY_UP:
            if direction != "down":
                direction = "up"
        elif k == curses.KEY_RIGHT:
            if direction != "left":
                direction = "right"
        elif k == curses.KEY_LEFT:
            if direction != "right":
                direction = "left"

        if direction == "up":
            cursor_y = cursor_y - 1
        elif direction == "down":
            cursor_y = cursor_y + 1
        elif direction == "left":
            cursor_x = cursor_x - 1
        elif direction == "right":
            cursor_x = cursor_x + 1

    	cursor_x = max(0, cursor_x)
    	cursor_x = min(width-2, cursor_x)

    	cursor_y = max(0, cursor_y)
    	cursor_y = min(height-1, cursor_y)

        for coord in snake_trail:
            if coord[0] == cursor_x:
                if coord[1] == cursor_y:
                    stdscr.addstr(5, 5, "you lose")
                    sys.exit()

        if len(snake_trail) <= snake_length:
            snake_trail.append([cursor_x,cursor_y])
        else:
            snake_trail.append([cursor_x,cursor_y])
            del snake_trail[0]

        if cursor_x == pellet_coords[0]:
            if cursor_y == pellet_coords[1]:
                #regen_pellet()
                pellet_coords = [random.randint(0, (width//2)), random.randint(0,height)]
                snake_length = snake_length + 4




        for coord in snake_trail[::-1]:
            if color_counter == 0:
                stdscr.attron(curses.color_pair(second_color))
                stdscr.addstr(coord[1], coord[0]*2, "  ")
                stdscr.attroff(curses.color_pair(second_color))
                color_counter = 1
            elif color_counter == 1:
                stdscr.attron(curses.color_pair(trail_color))
                stdscr.addstr(coord[1], coord[0]*2, "  ")
                stdscr.attroff(curses.color_pair(trail_color))
                color_counter = 2
            elif color_counter == 2:
                stdscr.attron(curses.color_pair(trail_color))
                stdscr.addstr(coord[1], coord[0]*2, "  ")
                stdscr.attroff(curses.color_pair(trail_color))
                color_counter = 0
        color_counter = 0

        #stdscr.addstr(0, 0, str(pellet_coords))

        stdscr.attron(curses.color_pair(pellet_color))
        stdscr.addstr(pellet_coords[1], pellet_coords[0]*2, "  ")
        stdscr.attroff(curses.color_pair(pellet_color))

    	stdscr.move(cursor_y, cursor_x*2 )
        stdscr.attron(curses.color_pair(cursor_color))
        stdscr.addstr(cursor_y, cursor_x*2, " ")
        stdscr.attroff(curses.color_pair(cursor_color))
    	stdscr.refresh()
    	k = stdscr.getch()

        time.sleep(.05)

def main():
	curses.wrapper(draw)

if __name__ == "__main__":
	main()
