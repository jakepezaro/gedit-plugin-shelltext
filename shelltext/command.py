from subprocess import run, PIPE, Popen
from typing import List, Dict


class ParserState:

    def __init__(self):
        self.commands = []
        self.pipes = [self.commands]
        self.current = ''
        self.quoted = None

    def start_quote(self, q: str):
        self.quoted = q
        self.next_command()

    def end_quote(self):
        self.quoted = None
        self.next_command()

    def create_pipe(self):
        self.commands = []
        self.pipes.append(self.commands)

    def append_command(self, c: str):
        self.current += c

    def next_command(self):
        if self.current != '':
            self.commands.append(self.current)
            self.current = ''


def parse_command(command: str) -> List[List[str]]:
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


def run_command(source_text: str, commands: List[List[str]], env: Dict[str, str]) -> str:
    print(commands[0])
    p1 = Popen(commands[0], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = p1.communicate(input=bytes(source_text, 'utf-8'), timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = p1.communicate()
    return str(outs, 'utf-8')

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
