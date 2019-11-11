import curses
from curses import wrapper
import time
import random


class Birdie:
    def __init__(self, y=5, downward_accl=0):
        self.y = y
        self.downward_accl = downward_accl  # downward acceleration

    def flap(self):
        self.y -= 3
        self.downward_accl = -1

    def update(self, counter):
        if counter % 2 == 0:
            self.y += 1 + self.downward_accl
        if counter % 10 == 0:
            self.downward_accl += 1

    def draw(self, stdscr):
        stdscr.addstr(self.y, 20, '>', curses.color_pair(2))
        stdscr.refresh()


class Pipe:
    def __init__(self, x=78, opening=None):
        if opening:
            self.opening = opening
        else:
            self.opening = random.randint(3, 14)
        self.x = x

    def update(self):
        self.x -= 1

    def draw(self, stdscr):
        for i in range(24):
            if i not in [i for i in range(self.opening, self.opening+7)]:
                stdscr.addstr(i, self.x, '█')
        stdscr.refresh()

    def karl_within(self, karl: Birdie):
        locations = []
        for i in range(24):
            if i not in [i for i in range(self.opening, self.opening+7)]:
                locations.append([i, self.x])

        return [karl.y, 20] in locations
    
    def karl_passing(self, karl: Birdie):
        locations = []
        for i in range(24):
            if i in [i for i in range(self.opening, self.opening+7)]:
                locations.append([i, self.x])

        return [karl.y, 20] in locations


def log(s):
    with open('log.txt', 'a') as l:
        l.write(str(s) + '\n')


def main(stdscr):
    karl = Birdie()
    pipes = []
    counter = 0
    points = 0
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    stdscr.nodelay(True)
    curses.curs_set(0)

    while True:
        stdscr.erase()

        k = stdscr.getch()
        if k == ord(' '):
            karl.flap()
        karl.update(counter)

        try: # throws error if karl is outside of stdscr
            karl.draw(stdscr) 
        except:
            return points

        for pipe in pipes:
            if pipe.x >= 0:
                pipe.draw(stdscr)
                pipe.update()
                if pipe.karl_within(karl):
                    return points
                if pipe.karl_passing(karl):
                    points += 1
            else:
                del pipe

        if counter % 40 == 0:
            pipes.append(Pipe())

        stdscr.addstr(0, 0, f'Points: {points}', curses.color_pair(3))
        stdscr.refresh()
        counter += 1
        time.sleep(0.04)


def death_message(points):
    if points == 0:
        print('What\'s wrong with you?? Eh??')
    elif points < 10:
        print('That\'s all you got!?')
    elif points < 30:
        print('You\'re getting a little better...')
    elif points < 50:
        print('Wowza! That\'s pretty darn good!')
    else:
        print('You must be a hacker.')


if __name__ == '__main__':    
    points = wrapper(main)
    print(f'Points: {points}')
    death_message(points)
    
