from shelltext.command import parse_command, run_command
import re

def test_single_command():
    assert parse_command('pwd') == [['pwd']]

def test_two_commands():
    assert parse_command('grep abc') == [['grep', 'abc']]

def test_double_quoted_separator_is_command():
    assert parse_command('sed "s/abc/d f/g"') == [['sed', 's/abc/d f/g']]

def test_single_quoted_separator_is_command():
    assert parse_command("sed 's/abc/d f/g'") == [['sed', 's/abc/d f/g']]

def test_double_quote_inside_single_quote_is_command():
    assert parse_command("sed 's/X/\"/g'") == [['sed', 's/X/"/g']]

def test_single_quote_inside_double_quote_is_command():
    assert parse_command('sed "s/X/\'/g"') == [['sed', 's/X/\'/g']]

def test_newline_is_separator():
    assert parse_command('pwd\nabc') == [['pwd', 'abc']]

def test_CR_is_separator():
    assert parse_command('pwd\rabc') == [['pwd', 'abc']]

def test_multiple_whitespace_collapsed():
    assert parse_command('pwd  \n \r abc') == [['pwd', 'abc']]

def test_pipe():
    assert parse_command('ls | grep abc') == [['ls'], ['grep', 'abc']]

def test_quoted_pipe_is_command():
    assert parse_command('echo "abc|def"') == [['echo', 'abc|def']]


def test_run_sed_no_pipe():
    input_text = strip_input('''
      |abc
      |def
    ''')
    assert run_command(input_text, [['sed', 's/bc/XX/g']], None) == 'aXX\ndef'


def test_run_grep_pipe_cat():
    input_text = strip_input('''
      |abc
      |def
    ''')
    assert run_command(input_text, [['grep', 'a'], ['cat']], None) == 'abc\n'


def test_run_sed_pipe_cat():
    input_text = strip_input('''
      |abc
      |def
    ''')
    assert run_command(input_text, [['sed', 's/ab/XX/g'], ['cat']], None) == 'XXc\ndef'


def test_run_command_without_pipe():
    input_text = strip_input('''
      |abc
      |def
    ''')
    assert run_command(input_text, [['grep', 'a']], None) == 'abc\n'


def test_run_command_with_pipe():
    input_text = strip_input('''
      |abc
      |def
    ''')
    assert run_command(input_text, [['sed', 's/bc/XX/g'], ['grep', 'X']], None) == 'aXX\n'


def test_run_command_with_2_pipes():
    input_text = strip_input('''
      |abc
      |abd
      |def
    ''')
    assert run_command(input_text, [['grep', 'd'], ['sed', 's/ab/XX/g']], None) == 'XXd\n'

FORMATTABLE = re.compile(r'^\s*\|(.*)$')

def strip_input(raw_text: str) -> str:
    lines = []
    for line in raw_text.split('\n'):
        m = FORMATTABLE.match(line)
        if m:
            lines.append(m.group(1))
    return '\n'.join(lines)
