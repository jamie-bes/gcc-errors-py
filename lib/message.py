import re
import dataclasses
from typing import Optional

@dataclasses.dataclass
class Message:
    filename: str
    line: int
    column: int
    msgtype: str
    text: str
    startIndex: int
    endIndex: int

    subtype: Optional[str] = None
    affectedSymbol: Optional[str] = None

    codeWhitespace: Optional[str] = None
    code: Optional[str] = None

    # Length in characters of the token where the error has occurred
    tokenLength: Optional[int] = None

    adjustedColumn: Optional[int] = None

    parentFunction: Optional[str] = None
    firstDefined: Optional[str] = None

    @staticmethod
    def fromGcc(components, stdout):
        startIndex = stdout.index(components[0])
        endIndex = startIndex + len(components[0])

        new_msg = Message(
            filename        = components[1],
            line            = int(components[2]),
            column          = int(components[3]),
            msgtype         = components[4],
            text            = components[5],
            startIndex      = startIndex,
            endIndex        = endIndex,
            codeWhitespace  = components[6] if components[6] else '',
            code            = components[7] if components[7] else '',
        )

        if components[8]:
            new_msg.tokenLength = len(components[8])

        new_msg.adjustedColumn = new_msg.column - len(new_msg.codeWhitespace)
        new_msg.parentFunction = new_msg._lookbackFunction(stdout, new_msg.startIndex)

        return new_msg

    @staticmethod
    def fromLinker(components, stdout):
        subtype = components[3]
        affectedSymbol = components[5]
        startIndex = stdout.index(components[0])
        endIndex = startIndex + len(components[0])

        new_msg = Message(
            filename        = components[1],
            line            = int(components[2]),
            column          = 0,
            msgtype         = "error",
            text            = subtype + ' ' + components[4] + ' "' + affectedSymbol + '"',
            startIndex      = startIndex,
            endIndex        = endIndex,
            subtype         = subtype,
            affectedSymbol  = affectedSymbol,
            parentFunction  = new_msg._lookbackFunction(stdout, new_msg.startIndex),
        )

        if new_msg.subtype == "multiple definition":
            new_msg.firstDefined = new_msg._lookupFirstDefinition(stdout, new_msg.endIndex)

        return new_msg

    def _matchAll(self, regex, input):
        return list(re.finditer(regex, input))

    def _lookbackFunction(self, stdout, index):
        regex = r"In function\s(`|')(.*)'"
        matches = self._matchAll(regex, stdout[0:index])
        if len(matches) > 0:
            return matches[-1][0][2]

    def _lookupFirstDefinition(self, stdout, index):
        regex = r":(.*):(\d+): first defined here"

        matches = self._matchAll(regex, stdout[0:index])
        if len(matches) > 0:
            location = {"filename": matches[0][1], "line": int(matches[0][2])}
            return location
