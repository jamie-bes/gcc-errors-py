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

    def fromGcc(components, stdout):
        self.filename = components[1]
        self.line = parseInt(components[2])
        self.column = parseInt(components[3])
        self.type = components[4]
        self.text = components[5]
        self.codeWhitespace = components[6] if components[6] else ''
        self.code = components[7] if components[7] else ''
        if (components[8]):
            self.tokenLength = components[8].length

        self.adjustedColumn = self.column - self.codeWhitespace.length
        self.startIndex = stdout.indexOf(components[0])
        self.endIndex = self.startIndex + components[0].length
        self.parentFunction = self._lookbackFunction(stdout, self.startIndex)

        return self

    def fromLinker(components, stdout):
        self.filename = components[1]
        self.line = parseInt(components[2])
        self.column = 0
        self.type = 'error'
        self.subtype = components[3]
        self.affectedSymbol = components[5]
        self.text = self.subtype + ' ' + components[4] + ' "' + self.affectedSymbol + '"'

        self.startIndex = stdout.indexOf(components[0])
        self.endIndex = self.startIndex + components[0].length
        self.parentFunction = self._lookbackFunction(stdout, self.startIndex)

        if (self.subtype == 'multiple definition'):
            self.firstDefined = self._lookupFirstDefinition(stdout, self.endIndex)

        return self

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
