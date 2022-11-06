from subprocess import run, PIPE


def parse_command(command):
    commands = []
    current = ''
    quoted = None
    for c in command:
       q = c if c in ['"', "'"] else None
       is_separator = c in [' ', '\n', '\r']
       is_pipe = c == '|'
       if not quoted and q:
           quoted = q
           if current.strip() != '':
               commands.append(current)
           current = ''
           continue
       if quoted and quoted == q:
           quoted = None
           if current != '':
               commands.append(current)
           current = ''
           continue
       if is_separator and not quoted:
           if current != '':
               commands.append(current)
           current = ''
           continue
       current += c
    if current != '':
        commands.append(current)
    return [commands]

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
