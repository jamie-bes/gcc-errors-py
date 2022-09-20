import re
import dataclasses

@dataclasses.dataclass
class Message:
    filename: str
    line: int
    column: int
    type: str
    subtype = None
    affectedSymbol = None
    text: str
    codeWhitespace = None
    code = None

    # Length in characters of the token where the error has occurred
    tokenLength = None

    adjustedColumn = None
    startIndex: int
    endIndex: int
    parentFunction = None
    firstDefined = None

    @staticmethod
    def fromGcc(components, stdout):
        filename = components[1]
        line = int(components[2])
        column = int(components[3])
        _type = components[4]
        text = components[5]
        startIndex = stdout.index(components[0])
        endIndex = startIndex + len(components[0])

        new_msg = Message(filename, line, column, _type, text, startIndex, endIndex)

        new_msg.codeWhitespace = components[6] if components[6] else ''
        new_msg.code = components[7] if components[7] else ''
        if components[8]:
            new_msg.tokenLength = len(components[8])

        new_msg.adjustedColumn = new_msg.column - len(new_msg.codeWhitespace)
        new_msg.parentFunction = new_msg._lookbackFunction(stdout, new_msg.startIndex)

        return new_msg

    @staticmethod
    def fromLinker(components, stdout):
        subtype = components[3]
        affectedSymbol = components[5]

        filename = components[1]
        line = int(components[2])
        column = 0
        _type = "error"
        text = subtype + ' ' + components[4] + ' "' + affectedSymbol + '"'
        startIndex = stdout.index(components[0])
        endIndex = startIndex + len(components[0])

        new_msg = Message(filename, line, column, _type, text, startIndex, endIndex)

        new_msg.subtype = subtype
        new_msg.affectedSymbol = affectedSymbol
        new_msg.parentFunction = new_msg._lookbackFunction(stdout, new_msg.startIndex)

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
