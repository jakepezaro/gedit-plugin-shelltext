from subprocess import run, PIPE


class ParserState:

    def __init__(self):
        self.commands = []
        self.pipes = [self.commands]
        self.current = ''
        self.quoted = None

    def start_quote(self, q):
        self.quoted = q
        self.next_command()

    def end_quote(self):
        self.quoted = None
        self.next_command()

    def create_pipe(self):
        self.commands = []
        self.pipes.append(self.commands)

    def append_command(self, c):
        self.current += c

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
        if not state.quoted and q:
            state.start_quote(q)
        elif state.quoted and state.quoted == q:
            state.end_quote()
        elif not state.quoted and is_separator:
            state.next_command()
        elif not state.quoted and is_pipe:
            state.create_pipe()
        else:
            state.append_command(c)
    state.next_command()
    return state.pipes

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
