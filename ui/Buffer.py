class Buffer(object):
    def __init__(self, window, lines):
        self.window = window
        self.lines = lines
        self.buffer = [""]

    def write(self, text):
        lines = text.split("\n")
        self.buffer[-1] += lines[0]
        self.buffer.extend(lines[1:])
        self.refresh()

    def writeln(self, text):
        self.write(text + "\n")

    def input(self, text = ""):
        return self._input(text, lambda: self.window.getstr().decode('utf-8'))

    def input_chr(self, text = ""):
        return self._input(text, lambda: chr(self.window.getch()))

    def _input(self, text, get_input):
        self.write(text)
        input = get_input()
        self.writeln(input)
        return input

    def refresh(self):
        self.window.clear()
        for nr, line in enumerate(self.buffer[-self.lines:]):
            self.window.addstr(nr, 0, line)