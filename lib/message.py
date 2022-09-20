class Message:
    def __init__(self, filename, line, column, type, text, startIndex, endIndex):
        self.filename: str = filename
        self.line: int = line
        self.column: int = column
        self.type: str = type
        self.subtype = None
        self.affectedSymbol = None
        self.text: str = text
        self.codeWhitespace = None
        self.code = None

        # Length in characters of the token where the error has occurred
        self.tokenLength = None

        self.adjustedColumn = None
        self.startIndex: int = startIndex
        self.endIndex: int = endIndex
        self.parentFunction = None
        self.firstDefined = None

    @staticmethod
    def fromGcc(components, stdout):
        new_msg = Message()

        new_msg.filename = components[1]
        new_msg.line = int(components[2])
        new_msg.column = int(components[3])
        new_msg.type = components[4]
        new_msg.text = components[5]
        new_msg.codeWhitespace = components[6] if components[6] else ''
        new_msg.code = components[7] if components[7] else ''
        if components[8]:
            new_msg.tokenLength = len(components[8])

        new_msg.adjustedColumn = new_msg.column - len(new_msg.codeWhitespace)
        new_msg.startIndex = stdout.index(components[0])
        new_msg.endIndex = new_msg.startIndex + len(components[0])
        new_msg.parentFunction = new_msg._lookbackFunction(stdout, new_msg.startIndex)

        return new_msg

    @staticmethod
    def fromLinker(components, stdout):
        new_msg = Message()

        new_msg.filename = components[1]
        new_msg.line = int(components[2])
        new_msg.column = 0
        new_msg.type = "error"
        new_msg.subtype = components[3]
        new_msg.affectedSymbol = components[5]
        new_msg.text = new_msg.subtype + ' ' + components[4] + ' "' + new_msg.affectedSymbol + '"'

        new_msg.startIndex = stdout.index(components[0])
        new_msg.endIndex = new_msg.startIndex + len(components[0])
        new_msg.parentFunction = new_msg._lookbackFunction(stdout, new_msg.startIndex)

        if new_msg.subtype == "multiple definition":
            new_msg.firstDefined = new_msg._lookupFirstDefinition(stdout, new_msg.endIndex)

        return new_msg

    def _matchAll(regex, input):
        match = None
        matches = []
        while ((match = regex.exec(input))):
            matches.push(match)

        return matches

    def _lookbackFunction(stdout, index):
        regex = /In function\s(`|')(.*)'/g
        matches = self._matchAll(regex, stdout.slice(0, index))
        if (matches.length):
            return matches.slice(-1)[0][2]

        return

    def _lookupFirstDefinition(stdout, index):
        regex = /:(.*):(\d+): first defined here/g

        matches = self._matchAll(regex, stdout.slice(index))
        if (matches.length):
            return {
                "filename": matches[0][1],
                "line": parseInt(matches[0][2])
            }
        return
