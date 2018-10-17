import os
import re
from glob import glob

from lark import Lark, Tree

parser = {}
for name in glob(os.path.join(os.path.dirname(__file__), "grammar", "*.g")):
    with open(name) as f:
        ver = tuple(
            int(n) for n in
            re.findall(r"\d+", str(os.path.basename(name).split(".g")[0]))
        )
        parser[ver] = Lark(f.read())

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, version=None):
        if version is None:
            self.version = sorted(parser.keys())[-1]
            self.lark = parser[self.version]
        elif version in parser:
            self.lark = parser[version]
            self.version = version
        else:
            raise ParserError("Unknown parser grammar version: {}"
                             .format(version))
        self.tree = None
        self.filter = None

    def parse(self, filter_):
        try:
            self.tree = self.lark.parse(filter_)
            self.filter = filter_
            return self.tree
        except Exception as e:
            raise ParserError(str(e))

    def __repr__(self):
        if isinstance(self.tree, Tree):
            return self.tree.pretty()
        else:
            return repr(self.lark)
