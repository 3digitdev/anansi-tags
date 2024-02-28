import re


_ESC = '\x1b['
_OPEN = {
    # Decoration
    'bold': '1',
    'dim': '2',
    'italic': '3',
    'under': '4',
    'blink': '5',
    'strike': '9',
    'frame': '51',
    'circle': '52',
    'overline': '53',
    # Foreground Colors
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    # Background Colors
    'bg_black': '40',
    'bg_red': '41',
    'bg_green': '42',
    'bg_yellow': '43',
    'bg_blue': '44',
    'bg_magenta': '45',
    'bg_cyan': '46',
}
_CLOSE = {
    # Decoration
    '/bold': '22',
    '/dim': '22',
    '/italic': '23',
    '/under': '24',
    '/blink': '25',
    '/strike': '29',
    '/frame': '54',
    '/circle': '54',
    '/overline': '55',
    # Foreground Colors
    '/fg': '39',
    # Background Colors
    '/bg': '49',
    # End all formatting
    '/': '0',
}
_LINK_PREFIX = '\x1b]8;;'
_LINK_SUFFIX = '\x1b\x5c'
# Matches all ansi regex tags that are supported in a string
_ANSI_REGEX = re.compile(r'\x1b\[\d+(;\d*)*m|\x1b]8;;[^\\]*\x1b\x5c')
# Captures the _formatting codes_ for the ANSI
_TAG_ANSI_BASIC_REGEX = re.compile(r'\x1b\[(\d+(?:;\d*)*)m')
# Captures the _link ref_ for the ANSI
_TAG_ANSI_LINK_REGEX = re.compile(r'\x1b]8;;([^\\]*)\x1b\x5c')
_TAG_ANSI_LINK_STRIP_REGEX = re.compile(r'\x1b]8;;([^\\]*)\x1b\x5c[^\x1b]*\x1b]8;;\x1b\x5c')
_ANSI = {**_OPEN, **_CLOSE}


def _parse_link(match: re.Match) -> str:
    url, text = match.groups()
    return _LINK_PREFIX + url + _LINK_SUFFIX + text + _LINK_PREFIX + _LINK_SUFFIX


def _strip_link(match: re.Match, keep_url: bool = False) -> str:
    return match.groups()[int(not keep_url)]


def _parse_basic_tags(match: re.Match) -> str:
    codes = match.groups()[0].split(';')
    tag_parts = []
    for code in codes:
        for k, v in _ANSI.items():
            if v == code:
                tag_parts.append(k)
                break
        else:
            raise ValueError(f'{code} is not a supported ANSI code')
    return f'[{" ".join(tag_parts)}]'


def _parse_links(match: re.Match) -> str:
    link_ref = match.groups()[0]
    return f'[link={link_ref}]' if link_ref else '[/link]'


def strip_ansi(ansi_str: str, keep_url: bool = False) -> str:
    if keep_url:
        ansi_str = _TAG_ANSI_LINK_STRIP_REGEX.sub(r'\1', ansi_str)
    return _ANSI_REGEX.sub('', ansi_str)


def parse_ansi(ansi_str: str) -> str:
    """Parses a string with ANSI codes and attempts to convert them to markdown"""
    tagged = _TAG_ANSI_BASIC_REGEX.sub(_parse_basic_tags, ansi_str)
    return _TAG_ANSI_LINK_REGEX.sub(_parse_links, tagged)
