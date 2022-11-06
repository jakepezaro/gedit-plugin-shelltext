from subprocess import run, PIPE


def parse_command(command):
    commands = []
    current = ''
    in_quote = False
    for c in command:
       is_quote = c == '"'
       is_separator = c == ' '
       if not in_quote and is_quote:
           in_quote = True
           if current.strip() != '':
               commands.append(current)
           current = ''
           continue
       if in_quote and is_quote:
           in_quote = False
           if current != '':
               commands.append(current)
           current = ''
           continue
       if is_separator and not in_quote:
           commands.append(current)
           current = ''
           continue
       current += c
    if current != '':
        commands.append(current)
    return commands

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
