# Anansi Tags

Apply simple BBCode-like tags to Python strings to get ANSI

_No frills.  No dependencies.  Just strings!_

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O7V0GB2)

## Installation

```shell
pip install anansi-tags
```

## Usage

This library aims to be as dead-simple as possible.  All functions take a string and return a string.
There are only 4 functions that you'll need to worry about as well, providing ways to convert back
and forth between ANSI and the custom tags, and even to strip either ANSI or the tags from a string.

### Simple Usage

Basic tags can be handled in a nice simple way:

```python
from anansi import parse_tags

print(parse_tags('[bold]Hello world[/bold]'))
```

You can make colored text.  Colored text ("foreground") is cancelled with `/fg`:

```python
from anansi import parse_tags

print(parse_tags('[red]Hello world[/fg]'))
```

You can do background colors.  Background colors are cancelled with `/bg`:

```python
from anansi import parse_tags

print(parse_tags('[bg_white]Hello world[/bg]'))
```

You can combine any of these to make some super complex tags too:
**Note:  You can cancel ALL formatting you have added so far with `[/]`!**

```python
from anansi import parse_tags

print(parse_tags('[yellow bg_green italic]Oh god this is unreadable[/]'))
```

**Let's get CRAZY**:

```python
from anansi import parse_tags

print(parse_tags('[yellow bg_green italic]Oh god this is [bold]unreadable[/bold /italic under] Please remove[/bg] the colors[/] oh thank you.'))
```

#### Hyperlinks

Anansi also supports hyperlinking, as long as your terminal does too:

```python
from anansi import parse_tags

print(parse_tags('[link=https://github.com/3digitdev/anansi-tags]Anansi[/link] is a very simple library!'))
```

You can even style hyperlinks!

```python
from anansi import parse_tags

print(parse_tags('[link=https://github.com/3digitdev/anansi-tags][bold]Anansi[/][/link] is a very simple library!'))
```

**Note:  Remember that you can't combine `link` tags with any other type of tag!  They are incompatible.**

### ANSI-Strings → Anansi Tags

This will work for all supported Anansi tags, including links:

```python
from anansi import parse_ansi

# Yep, ansi is ugly.
print(parse_ansi('\x1b[1mHello\x1b[22m'))
# Result:  '[bold]Hello[/bold]'
```

### Stripping Anansi Tags

```python
from anansi import strip_tags

print(strip_tags('[bold]Hello[/bold]'))
# Result:  'Hello'
```

If you strip a hyperlink, by default it will remove the URL, leaving only the text:

```python
from anansi import strip_tags

print(strip_tags('[link=www.google.com]A link to Google[/link]'))
# Result:  'A link to Google'
```

You can configure this behavior with `keep_url`:

```python
from anansi import strip_tags

print(strip_tags('[link=www.google.com]A link to Google[/link]', keep_url=True))
# Result:  'www.google.com'
```

### Stripping ANSI codes

```python
from anansi import strip_ansi

print(strip_ansi('\x1b[1mHello\x1b[22m'))
# Result:  'Hello'
```

Just like with `strip_tags()`, stripping a hyperlink removes the URL, leaving only the text:

```python
from anansi import strip_ansi

print(strip_ansi('\x1b]8;;www.google.com\x1b\x5cA link to Google\x1b]8;;\x1b\x5c'))
# Result:  'A link to Google'
```

Also, just like with `strip_tags()`, you can tell `strip_ansi()` to only keep the URL:

```python
from anansi import strip_ansi

print(strip_ansi('\x1b]8;;www.google.com\x1b\x5cA link to Google\x1b]8;;\x1b\x5c', keep_url=True))
# Result:  'www.google.com'
```

## FAQ

### Didn't you know that {other library} supports this?

I probably didn't tbh -- I didn't look too hard.  Odds are though that whatever library you're thinking
of probably is much bigger with way more features and support and fanciness to it.  If that's better for
you, then great!   

My intention here was to create a no-frills way to just...deal with strings.  I found this 
**surprisingly difficult** in other similar works, and that's what prompted me to write Anansi!

### Why do you only support 8 colors??

Honestly, if you have a need for the difference between `216` ("light_salmon1") and `217` ("light_pink1"),
it's likely that your needs are severely more complex than what I intended for this library.  I highly
rcommend you go check out awesome libraries like [Rich](https://github.com/Textualize/rich) instead!

### Why don't you support {other ANSI code}

Kinda the same reason as above?  There's a lot of ANSI stuff out there, and this library is really just
for the most basic usage that you should usually need I think.

### {Supported ANSI code} isn't doing anything!

Yeah I added some in despite them not being widely supported.  Of note, I've found that `blink`, `frame`,
`circle`, and `overline` all seem to just...do nothing for me too?  Using `iTerm` over here.  Maybe some support
it so I wanted them as options I guess, but your mileage may vary, sorry!  Terminal standards are all over the place.

### My link is acting weird

I haven't done much thorough testing of links, and url-encoding is another complex standard.  If you find
scenarios that don't work feel free to open an issue!  I can't promise I'll make supporting URL standards
a full priority, but it doesn't hurt to ask!
