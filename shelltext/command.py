from subprocess import run, PIPE


class ParserState:

    def __init__(self):
        self.commands= []
        self.current = ''
        self.quoted = None

    def start_quote(self, q):
        if not self.quoted and q:
            self.quoted = q
            self.next_command()
            return True

    def end_quote(self, q):
        if self.quoted and self.quoted == q:
            self.quoted = None
            self.next_command()
            return True

    def end_command(self, is_separator):
        if not self.quoted and is_separator:
            self.next_command()
            return True

    def pipe(self, is_pipe):
        return False

    def append_command(self, c):
        self.current += c
        return True

    def next_command(self):
        if self.current != '':
            self.commands.append(self.current)
            self.current = ''


def parse_command(command):
    state = ParserState()
    for c in command:
        q = c if c in ['"', "'"] else None
        is_separator = c in [' ', '\n', '\r']
        is_pipe = c == '|'
        if state.start_quote(q):
            pass
        elif state.end_quote(q):
            pass
        elif state.end_command(is_separator):
            pass
        elif state.pipe(is_pipe):
            pass
        else:
            state.append_command(c)
    state.next_command()
    return [state.commands]

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
