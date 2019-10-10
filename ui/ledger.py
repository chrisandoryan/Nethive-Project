import os
from ui.Buffer import Buffer
import curses
import time

class MainPanel:
    stdscr = None

    lines = 50
    columns = 200
    quarterWidth = int(columns / 4)

    elkwindow = None
    elkbuffer = None
    logwindow = None
    logbuffer = None # Buffer(logwindow, lines)

    def __init__(self, stdscr):
        curses.echo()
        self.stdscr = stdscr
        nrows, ncols = 50, 200 # stdscr.getmaxyx()
        self.lines = nrows
        self.columns = ncols

        self.logwindow = curses.newwin(self.lines, self.quarterWidth * 3)
        self.elkwindow = curses.newwin(self.lines, self.quarterWidth, 0, self.quarterWidth * 3 + 2)

        self.elkbuffer = Buffer(self.elkwindow, self.lines)
        self.logbuffer = Buffer(self.logwindow, self.lines)

    def out2elk(self, buffer):
        self.elkbuffer.writeln(buffer)

    def out2log(self, buffer):
        self.logbuffer.writeln(buffer)

    def refresh(self):
        self.logbuffer.refresh()
        self.elkbuffer.refresh()
        self.stdscr.refresh()

    def run(self):
        while True:
            self.refresh()
            time.sleep(1)

    def close(self):
        curses.endwin()

    # def run(self, stdscr):
    #     left_window.border(2)
    #     left_window.box()
    #     left_buffer = Buffer(left_window, lines)
    #     left_buffer.writeln('LEFT')
    #     left_buffer.refresh()
    #     left_buffer.input_chr()
    #     right_window = curses.newwin(lines, half_width, 0, half_width + 2)
    #     right_window.border(2)
    #     right_window.box()
    #     right_buffer = Buffer(right_window, lines)
    #     right_buffer.writeln('RIGHT')
    #     right_buffer.refresh()
    #     right_buffer.input_chr()