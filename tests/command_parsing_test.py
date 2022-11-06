from shelltext.command import parse_command

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

#def test_pipe():
#    assert parse_command('ls | grep abc') == [['ls'], ['grep', 'abc']]
