"""
Generic parsers for vmware configuration text files
"""

import numbers

from stellator.constants import *

class FileParserError(Exception):
    pass


class IndexedConfigEntry(object):
    """Indexed object

    Sortable parent class for indexed objects.
    """

    def __init__(self, index):
        self.index = int(index)

    def __cmp__(self, other):
        if isinstance(other, numbers.Number):
            return cmp(self.index, other)

        if isinstance(other, basestring):
            return cmp(self.index, int(other))

        return cmp(self.index, other.index)


class VMWareConfigFileParser(object):
    """Configuration parser

    Parser for vmware text configuration files, like .vmx or library inventory
    """
    def __init__(self, path):
        self.path = path
        self.meta = {}

    def load(self):
        try:
            with open(self.path, 'r') as fd:
                for line in sorted(line.strip() for line in fd.readlines()):
                    self.parse_line(line)
        except OSError, (ecode, emsg):
            raise FileParserError('Error reading {0}: {1}'.format(self.path, emsg))
        except IOError, (ecode, emsg):
            raise FileParserError('Error reading {0}: {1}'.format(self.path, emsg))

    def parse_line(self, line):
        """Split key, value line

        Expects lines to be of key = value format, calling self.parse_value for
        the detected entries. Ignores anything else.
        """
        try:
            key, value = [x.strip() for x in line.split('=', 1)]
        except ValueError:
            return
        value = value.strip('"')
        return self.parse_value(key, value)

    def parse_value(self, key, value):
        """Parse key, value pair

        Parses common options for all files. Returns True if value was parsed.
        """
        if key in CONFIG_META_KEYS:
            self.meta[CONFIG_META_KEYS[key]] = value
            return True

        return False
