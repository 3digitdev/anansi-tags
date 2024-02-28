import re

from anansi.ansi import _ANSI, _ESC, _parse_link, _strip_link


_TAG_REGEX = re.compile(rf'(\[(?:(?:(?:{"|".join(_ANSI.keys())})\s*)*)+])')
_LINK_REGEX = re.compile(r'\[link=(?P<url>[^]]*)](?P<txt>.*)\[/link]')


def _parse_tags(cmd: re.Match) -> str:
    cmd = cmd.groups()[0]
    contents = cmd.strip('[').strip(']')
    tags = contents.split(' ')
    for i, tag in enumerate(tags):
        code = _ANSI.get(tag)
        if not code:
            continue
        tags[i] = code
    return f'{_ESC}{";".join(tags)}m'


def parse_tags(tag_str: str) -> str:
    tags_parsed = _TAG_REGEX.sub(_parse_tags, tag_str)
    return _LINK_REGEX.sub(_parse_link, tags_parsed)


def strip_tags(line: str, keep_url: bool = False) -> str:
    tagged = _TAG_REGEX.sub('', line)
    return _LINK_REGEX.sub(lambda m: _strip_link(m, keep_url), tagged)
