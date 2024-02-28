import pytest

from anansi import parse_ansi, parse_md, strip_ansi, strip_md
from tests.conftest import TestString


@pytest.mark.parametrize(
    'fixture_name',
    [
        'basic',
        'multi_tag_global',
        'multi_tag_separate',
        'multi_tag_close_open',
        'complex',
        'hyperlink',
        'hyperlink_with_md',
    ],
)
def test_parse_ansi(fixture_name: str, request):
    test_entry: TestString = request.getfixturevalue(fixture_name)
    assert parse_ansi(test_entry.ansi) == test_entry.md, f'Conversion failed for {test_entry.desc}'


@pytest.mark.parametrize(
    'fixture_name',
    [
        'basic',
        'multi_tag_global',
        'multi_tag_separate',
        'multi_tag_close_open',
        'complex',
        'hyperlink',
        'hyperlink_with_md',
    ],
)
def test_strip_ansi(fixture_name: str, request):
    test_entry: TestString = request.getfixturevalue(fixture_name)
    assert strip_ansi(test_entry.ansi) == test_entry.stripped, f'Conversion failed for {test_entry.desc}'


def test_strip_ansi_keep_url(hyperlink_keep_url: TestString):
    actual = strip_ansi(hyperlink_keep_url.ansi, keep_url=True)
    assert actual == hyperlink_keep_url.stripped, f'Conversion failed for {hyperlink_keep_url.desc}'


@pytest.mark.parametrize(
    'fixture_name',
    [
        'basic',
        'multi_tag_global',
        'multi_tag_separate',
        'multi_tag_close_open',
        'complex',
        'hyperlink',
        'hyperlink_with_md',
    ],
)
def test_parse_md(fixture_name: str, request):
    test_entry: TestString = request.getfixturevalue(fixture_name)
    actual = parse_md(test_entry.md)
    print(f'Actual parsed string: [{actual}]')
    assert actual == test_entry.ansi, f'Conversion failed for {test_entry.desc}'


@pytest.mark.parametrize(
    'fixture_name',
    [
        'basic',
        'multi_tag_global',
        'multi_tag_separate',
        'multi_tag_close_open',
        'complex',
        'hyperlink',
        'hyperlink_with_md',
    ],
)
def test_strip_md(fixture_name: str, request):
    test_entry: TestString = request.getfixturevalue(fixture_name)
    assert strip_md(test_entry.md) == test_entry.stripped, f'Conversion failed for {test_entry.desc}'


def test_strip_md_keep_url(hyperlink_keep_url: TestString):
    actual = strip_md(hyperlink_keep_url.md, keep_url=True)
    assert actual == hyperlink_keep_url.stripped, f'Conversion failed for {hyperlink_keep_url.desc}'
