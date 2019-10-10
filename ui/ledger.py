import os
from ui.Buffer import Buffer
import curses

def run(stdscr):
    curses.echo()

    lines = 50
    columns = 200

    half_width = int(columns / 2)

    left_window = curses.newwin(lines, half_width)
    left_window.border(2)
    left_window.box()
    left_buffer = Buffer(left_window, lines)

    # left_buffer.writeln('LEFT')
    left_buffer.refresh()
    left_buffer.input_chr()

    right_window = curses.newwin(lines, half_width, 0, half_width + 2)
    right_window.border(2)
    right_window.box()
    right_buffer = Buffer(right_window, lines)

    # right_buffer.writeln('RIGHT')
    right_buffer.refresh()
    right_buffer.input_chr()