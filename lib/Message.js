'use strict';

class Message {
    fromGcc(components, stdout) {
        self.filename = components[1];
        self.line = parseInt(components[2]);
        self.column = parseInt(components[3]);
        self.type = components[4];
        self.text = components[5];
        self.codeWhitespace = components[6] ? components[6] : '';
        self.code = components[7] ? components[7] : '';
        if (components[8]) {
            self.tokenLength = components[8].length;
        }

        self.adjustedColumn = self.column - self.codeWhitespace.length;
        self.startIndex = stdout.indexOf(components[0]);
        self.endIndex = self.startIndex + components[0].length;
        self.parentFunction = self._lookbackFunction(stdout, self.startIndex);

        return self;
    }

    fromLinker(components, stdout) {
        self.filename = components[1];
        self.line = parseInt(components[2]);
        self.column = 0;
        self.type = 'error';
        self.subtype = components[3];
        self.affectedSymbol = components[5];
        self.text = self.subtype + ' ' + components[4] + ' "' + self.affectedSymbol + '"';

        self.startIndex = stdout.indexOf(components[0]);
        self.endIndex = self.startIndex + components[0].length;
        self.parentFunction = self._lookbackFunction(stdout, self.startIndex);

        if (self.subtype === 'multiple definition') {
            self.firstDefined = self._lookupFirstDefinition(stdout, self.endIndex);
        }

        return self;
    }

    _matchAll(regex, input) {
        let match = null;
        const matches = [];
        while ((match = regex.exec(input))) {
            matches.push(match);
        }
        return matches;
    }

    _lookbackFunction(stdout, index) {
        const regex = /In function\s(`|')(.*)'/g;
        const matches = self._matchAll(regex, stdout.slice(0, index));
        if (matches.length) {
            return matches.slice(-1)[0][2];
        }
        return;
    }

    _lookupFirstDefinition(stdout, index) {
        const regex = /:(.*):(\d+): first defined here/g;

        const matches = self._matchAll(regex, stdout.slice(index));
        if (matches.length) {
            return {
                filename: matches[0][1],
                line: parseInt(matches[0][2])
            };
        }
        return;
    }
}

module.exports = Message;
