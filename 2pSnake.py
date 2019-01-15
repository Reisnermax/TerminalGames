#!/usr/bin/env
import curses
import random
import time
import copy

def draw(stdscr):
    key = 0
    timer = 0
    winner = None
    players = []
    pellets = []

    height, width = stdscr.getmaxyx()
    width = width // 2
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()

    green = 1
    magenta = 2
    red = 3
    cyan = 4
    yellow = 5
    wintext = 6
    black = 7
    blue = 8
    white = 9

    curses.init_pair(green, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(magenta, curses.COLOR_MAGENTA, curses. COLOR_MAGENTA)
    curses.init_pair(red, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(cyan, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(yellow, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(black, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(blue, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(white, curses.COLOR_WHITE, curses.COLOR_WHITE)


    curses.init_pair(wintext, curses.COLOR_YELLOW, curses.COLOR_CYAN)

    stdscr.nodelay(1)



    class pellet:
        def __init__(self):
            self.coords = [random.randint(1, width-3), random.randint(1, height-2)]

        def draw(self):
            stdscr.attron(curses.color_pair(cyan))
            stdscr.addstr(self.coords[1], self.coords[0] * 2, "  ")
            stdscr.attroff(curses.color_pair(cyan))

        def regen(self):
            self.coords = [random.randint(1, width-3), random.randint(1, height-2)]


    class snake:

        def __init__(self, name, control_string, color, seccolor, init_direction, init_coords, init_length):
            self.name = name
            self.control_string = control_string
            self.color = color
            self.sec_color = seccolor
            self.direction = init_direction
            self.head_coords = init_coords
            self.length = init_length
            self.color_counter = 0
            self.snake_trail = []

        def move(self):
            if self.direction == "up":
                self.head_coords[1] = self.head_coords[1] - 1
            elif self.direction == "down":
                self.head_coords[1] = self.head_coords[1] + 1
            elif self.direction == "left":
                self.head_coords[0] = self.head_coords[0] - 1
            elif self.direction == "right":
                self.head_coords[0] = self.head_coords[0] + 1

            self.head_coords[0] = max(0, self.head_coords[0])
            self.head_coords[0] = min(width-2, self.head_coords[0])

            self.head_coords[1] = max(0, self.head_coords[1])
            self.head_coords[1] = min(height-1, self.head_coords[1])

        def update_tail(self):
            self.snake_trail.append(copy.copy(self.head_coords))
            if len(self.snake_trail) >= self.length:
                del self.snake_trail[0]

        def draw(self):
            for coord in self.snake_trail[::-1]:
                stdscr.attron(curses.color_pair(white))
                stdscr.addstr(self.head_coords[1], self.head_coords[0]*2, "  ")
                stdscr.attroff(curses.color_pair(white))
                if self.color_counter == 0:
                    stdscr.attron(curses.color_pair(self.sec_color))
                    stdscr.addstr(coord[1], coord[0]*2, "  ")
                    stdscr.attroff(curses.color_pair(self.sec_color))
                    self.color_counter = 1
                elif self.color_counter == 1:
                    stdscr.attron(curses.color_pair(self.color))
                    stdscr.addstr(coord[1], coord[0]*2, "  ")
                    stdscr.attroff(curses.color_pair(self.color))
                    self.color_counter = 2
                elif self.color_counter == 2:
                    stdscr.attron(curses.color_pair(self.color))
                    stdscr.addstr(coord[1], coord[0]*2, "  ")
                    stdscr.attroff(curses.color_pair(self.color))
                    self.color_counter = 0

        def check_for_collisions(self):
            if self.head_coords[1] == 0 or self.head_coords[1] == height - 1:
                return True
            if self.head_coords[0] == 0 or self.head_coords[0] == width - 2:
                return True
            for tail in self.snake_trail:
                if self.head_coords == tail:
                    return True
            for player in players:
                for tail in player.snake_trail[:len(player.snake_trail)-1]:
                    if self.head_coords == tail:
                        return True
            for pellet in pellets:
                if self.head_coords == pellet.coords:
                    self.length = self.length + 6
                    pellet.regen()

        def key_check(self, key):
            if self.control_string != "ARROW":
                if key == ord(self.control_string[2]):
                    if self.direction != "up":
                        self.direction = "down"
                elif key == ord(self.control_string[0]):
                    if self.direction != "down":
                        self.direction = "up"
                elif key == ord(self.control_string[3]):
                    if self.direction != "left":
                        self.direction = "right"
                elif key == ord(self.control_string[1]):
                    if self.direction != "right":
                        self.direction = "left"
            else:
                if key == curses.KEY_DOWN:
                    if self.direction != "up":
                        self.direction = "down"
                elif key == curses.KEY_UP:
                    if self.direction != "down":
                        self.direction = "up"
                elif key == curses.KEY_RIGHT:
                    if self.direction != "left":
                        self.direction = "right"
                elif key == curses.KEY_LEFT:
                    if self.direction != "right":
                        self.direction = "left"

        def auto(self):
            self.update_tail()
            self.move()
            self.draw()


    def draw_border():
        stdscr.attron(curses.color_pair(red))
        for y in range(0,height):
            stdscr.addstr(y,0, "  ")
            stdscr.addstr(y, (width*2)-4, "  ")
        for x in range(2,width):
            stdscr.addstr(0, (x * 2) - 4, "  ")
            stdscr.addstr(height-1, (x * 2) - 4 , "  ")
        stdscr.attroff(curses.color_pair(red))



    players.append(snake("Green", "wasd", green, red, "right", [1,1], 10))
    players.append(snake("Yellow", "ARROW", yellow, cyan, "left", [width-3, height-2], 10))
    players.append(snake("Blue", "ijkl", blue, magenta, "down", [width-3, 1], 10))

    pellets.append(pellet())



    while key != ord('q'):

    	stdscr.clear()

        if winner == None:
            
            for player in range(0, len(players)):
                players[player].key_check(key)

            for player in range(0, len(players)):
                players[player].auto()

            for pelletz in pellets:
                pelletz.draw()

            if timer >= 5:
                pellets.append(pellet())
                timer = 0

            draw_border()

            to_delete = []

            for player in range(0, len(players)):
                if players[player].check_for_collisions() == True:
                    to_delete.append(player)

            for delt in to_delete[::-1]:
                del players[delt]

            if len(players) == 1:
                winner = players[0].name

        else:
            stdscr.clear()
            win_message = str(winner + " won")
            stdscr.attron(curses.color_pair(6))
            stdscr.addstr(height//2, width - (len(win_message)/2), win_message, curses.A_BLINK)
            stdscr.attroff(curses.color_pair(6))

        stdscr.refresh()
    	key = stdscr.getch()

        time.sleep(.05)
        timer = timer + .05


def main():
    curses.wrapper(draw)

if __name__ == "__main__":
	main()
