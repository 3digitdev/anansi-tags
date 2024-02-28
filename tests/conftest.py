import pytest

from dataclasses import dataclass


@dataclass
class TestString:
    ansi: str
    md: str
    stripped: str
    desc: str


@pytest.fixture
def basic():
    return TestString(md='[bold]Hello[/bold]', ansi='\x1b[1mHello\x1b[22m', stripped='Hello', desc='basic tag')


@pytest.fixture
def multi_tag_global():
    return TestString(
        md='[bold red]Hello[/]', ansi='\x1b[1;31mHello\x1b[0m', stripped='Hello', desc='multi-tag with global close'
    )


@pytest.fixture
def multi_tag_separate():
    return TestString(
        md='[bold red]Hello[/bold /fg]',
        ansi='\x1b[1;31mHello\x1b[22;39m',
        stripped='Hello',
        desc='multi-tag with separate close',
    )


@pytest.fixture
def multi_tag_close_open():
    return TestString(
        md='[bold red]Hello[/bold] world[/]',
        ansi='\x1b[1;31mHello\x1b[22m world\x1b[0m',
        stripped='Hello world',
        desc='multi-tag closing in separate tags',
    )


@pytest.fixture
def complex():
    return TestString(
        md='[bold red bg_black]Hello[/bold italic] world[/fg white] how are[/] you?',
        ansi='\x1b[1;31;40mHello\x1b[22;3m world\x1b[39;37m how are\x1b[0m you?',
        stripped='Hello world how are you?',
        desc='complex markdown with multiple open/close tags',
    )


@pytest.fixture
def hyperlink():
    return TestString(
        md='[link=www.google.com]A link to Google[/link]',
        ansi='\x1b]8;;www.google.com\x1b\x5cA link to Google\x1b]8;;\x1b\x5c',
        stripped='A link to Google',
        desc='a simple hyperlink',
    )


@pytest.fixture
def hyperlink_keep_url():
    return TestString(
        md='A link to [link=www.google.com]Google[/link]',
        ansi='A link to \x1b]8;;www.google.com\x1b\x5cGoogle\x1b]8;;\x1b\x5c',
        stripped='A link to www.google.com',
        desc='a simple hyperlink',
    )


@pytest.fixture
def hyperlink_with_md():
    return TestString(
        md='[link=www.google.com]A link to [bold]Google[/][/link]',
        ansi='\x1b]8;;www.google.com\x1b\x5cA link to \x1b[1mGoogle\x1b[0m\x1b]8;;\x1b\x5c',
        stripped='A link to Google',
        desc='a hyperlink with markdown in it',
    )
