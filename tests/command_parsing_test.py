from shelltext.command import parse_command

def test_split_commmand():
    assert parse_command('pwd') == ['pwd']
    assert parse_command('grep abc') == ['grep', 'abc']
    assert parse_command('sed "s/abc/d f/g"') == ['sed', 's/abc/d f/g']
    assert parse_command("sed 's/abc/d f/g'") == ['sed', 's/abc/d f/g']
