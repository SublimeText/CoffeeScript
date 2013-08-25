"""
sourcemap.decoder
~~~~~~~~~~~~~~~~~

Includes source from:
    https://github.com/martine/python-sourcemap
Original source under Apache license, see:
    https://github.com/martine/python-sourcemap/blob/master/COPYING

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
import os
import sys
from functools import partial
from .exceptions import SourceMapDecodeError
from .objects import Token, SourceMapIndex
try:
    import simplejson as json
except ImportError:
    import json  #NOQA

__all__ = ('SourceMapDecoder',)

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3
text_type = str if PY3 else unicode


class SourceMapDecoder(object):
    def parse_vlq(self, segment):
        """
        Parse a string of VLQ-encoded data.

        Returns:
          a list of integers.
        """

        values = []

        cur, shift = 0, 0
        for c in segment:
            val = B64[ord(c)]
            # Each character is 6 bits:
            # 5 of value and the high bit is the continuation.
            val, cont = val & 0b11111, val >> 5
            cur += val << shift
            shift += 5

            if not cont:
                # The low bit of the unpacked value is the sign.
                cur, sign = cur >> 1, cur & 1
                if sign:
                    cur = -cur
                values.append(cur)
                cur, shift = 0, 0

        if cur or shift:
            raise SourceMapDecodeError('leftover cur/shift in vlq decode')

        return values

    def decode(self, source):
        """Decode a source map object into a SourceMapIndex.

        The index is keyed on (dst_line, dst_column) for lookups,
        and a per row index is kept to help calculate which Token to retrieve.

        For example:
            A minified source file has two rows and two tokens per row.

            # All parsed tokens
            tokens = [
                Token(dst_row=0, dst_col=0),
                Token(dst_row=0, dst_col=5),
                Token(dst_row=1, dst_col=0),
                Token(dst_row=1, dst_col=12),
            ]

            Two dimentional array of columns -> row
            rows = [
                [0, 5],
                [0, 12],
            ]

            Token lookup, based on location
            index = {
                (0, 0):  tokens[0],
                (0, 5):  tokens[1],
                (1, 0):  tokens[2],
                (1, 12): tokens[3],
            }

            To find the token at (1, 20):
              - Check if there's a direct hit on the index (1, 20) => False
              - Pull rows[1] => [0, 12]
              - bisect_right to find the closest match:
                  bisect_right([0, 12], 20) => 2
              - Fetch the column number before, since we want the column
                lte to the bisect_right: 2-1 => row[2-1] => 12
              - At this point, we know the token location, (1, 12)
              - Pull (1, 12) from index => tokens[3]
        """
        # According to spec (https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#heading=h.h7yy76c5il9v)
        # A SouceMap may be prepended with ")]}'" to cause a Javascript error.
        # If the file starts with that string, ignore the entire first line.
        if source[:3] == ')]}':
            source = source.split('\n', 1)[1]

        smap = json.loads(source)
        sources = smap['sources']
        sourceRoot = smap.get('sourceRoot')
        names = list(map(text_type, smap['names']))
        mappings = smap['mappings']
        lines = mappings.split(';')

        # if sourceRoot is not None:
        #     sources = map(partial(os.path.join, sourceRoot), sources)

        # List of all tokens
        tokens = []

        # line_index is used to identify the closest column when looking up a token
        line_index = []

        # Main index of all tokens
        # The index is keyed on (line, column)
        index = {}

        dst_col, src_id, src_line, src_col, name_id = 0, 0, 0, 0, 0
        for dst_line, line in enumerate(lines):
            # Create list for columns in index
            line_index.append([])

            segments = line.split(',')
            dst_col = 0
            for segment in segments:
                if not segment:
                    continue
                parse = self.parse_vlq(segment)
                dst_col += parse[0]

                src = None
                name = None
                if len(parse) > 1:
                    try:
                        src_id += parse[1]
                        src = sources[src_id]
                        src_line += parse[2]
                        src_col += parse[3]

                        if len(parse) > 4:
                            name_id += parse[4]
                            name = names[name_id]
                    except IndexError:
                        raise SourceMapDecodeError

                # lol for now
                try:
                    assert dst_line >= 0
                    assert dst_col >= 0
                    assert src_line >= 0
                    assert src_col >= 0
                except AssertionError:
                    raise SourceMapDecodeError

                token = Token(dst_line, dst_col, src, src_line, src_col, name)
                tokens.append(token)

                # Insert into main index
                index[(dst_line, dst_col)] = token

                # Insert into specific line index
                line_index[dst_line].append(dst_col)

        return SourceMapIndex(smap, tokens, line_index, index, sources)


# Mapping of base64 letter -> integer value.
# This weird list is being allocated for faster lookups
B64 = [-1] * 123
for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'):
    B64[ord(c)] = i
