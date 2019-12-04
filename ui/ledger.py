# import os
# from ui.Buffer import Buffer
# import curses
# import time

# class MainPanel:
#     stdscr = None

#     lines = 50
#     columns = 200
#     quarterWidth = int(columns / 4)

#     outerr_window = None
#     outerr_buffer = None
#     logger_window = None
#     logger_buffer = None # Buffer(logger_window, lines)

#     def __init__(self, stdscr):
#         curses.echo()
#         self.stdscr = stdscr
#         nrows, ncols = 50, 200 # stdscr.getmaxyx()
#         self.lines = nrows
#         self.columns = ncols

#         self.logger_window = curses.newwin(self.lines, self.quarterWidth * 3)
#         self.logger_window.box()

#         self.outerr_window = curses.newwin(self.lines, self.quarterWidth, 0, self.quarterWidth * 3 + 2)
#         self.outerr_window.box()

#         self.outerr_buffer = Buffer(self.outerr_window, self.lines)
#         self.logger_buffer = Buffer(self.logger_window, self.lines)

#     def out2outerr(self, buffer):
#         self.outerr_buffer.writeln(buffer)

#     def out2logger(self, buffer):
#         self.logger_buffer.writeln(buffer)

#     def refresh(self):
#         self.logger_buffer.refresh()
#         self.outerr_buffer.refresh()
#         self.stdscr.refresh()

#     def run(self):
#         self.refresh()

#     def close(self):
#         curses.endwin()

#     # def run(self, stdscr):
#     #     left_window.border(2)
#     #     left_window.box()
#     #     left_buffer = Buffer(left_window, lines)
#     #     left_buffer.writeln('LEFT')
#     #     left_buffer.refresh()
#     #     left_buffer.input_chr()
#     #     right_window = curses.newwin(lines, half_width, 0, half_width + 2)
#     #     right_window.border(2)
#     #     right_window.box()
#     #     right_buffer = Buffer(right_window, lines)
#     #     right_buffer.writeln('RIGHT')
#     #     right_buffer.refresh()
#     #     right_buffer.input_chr()