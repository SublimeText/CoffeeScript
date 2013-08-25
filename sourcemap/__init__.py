"""
sourcemap
~~~~~~~~~

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
from .exceptions import SourceMapDecodeError  #NOQA
from .decoder import SourceMapDecoder

__version__ = '0.1.7'


def load(fp, cls=None):
    "Parse a sourcemap from a file-like object"
    return loads(fp.read(), cls)


def loads(source, cls=None):
    "Parse a sourcemap from a string"
    cls = cls or SourceMapDecoder
    return cls().decode(source)


def discover(source):
    "Given a JavaScript file, find the sourceMappingURL line"
    source = source.splitlines()
    # Source maps are only going to exist at either the top or bottom of the document.
    # Technically, there isn't anything indicating *where* it should exist, so we
    # are generous and assume it's somewhere either in the first or last 5 lines.
    # If it's somewhere else in the document, you're probably doing it wrong.
    if len(source) > 10:
        possibilities = source[:5] + source[-5:]
    else:
        possibilities = source

    for line in set(possibilities):
        pragma = line[:21]
        if pragma == '//# sourceMappingURL=' or pragma == '//@ sourceMappingURL=':
            # We want everything AFTER the pragma, which is 21 chars long
            return line[21:].rstrip()
    # XXX: Return None or raise an exception?
    return None
