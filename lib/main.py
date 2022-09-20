import message

def parseString(stdout):
    stdout = stdout.toString();

    messages = [*parseGcc(stdout), *parseLinker(stdout)];

    return messages;


def parseGcc(stdout):
    messages = [];
    match = None;
    deepRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(\s+)\d*\s*[|]*\s*(.*)\s+[|]*\s*(~*\^~*)/gm;
    #                  ^             ^     ^       ^             ^        ^    |            ^             ^
    #                  |             |     |       |             |        |    |            |             +- token marker
    #                  |             |     |       |             |        |    |            +- affected code
    #                  |             |     |       |             |        |    +- optional gcc 9.2 markup
    #                  |             |     |       |             |        +- whitespace before code
    #                  |             |     |       |             +- message text
    #                  |             |     |       +- type (error|warning|note)
    #                  |             |     +- column
    #                  |             +- line
    #                  +- filename
    while ((match = deepRegex.exec(stdout))):
        messages.push(new Message().fromGcc(match, stdout));

    simpleRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(?!\s)/gm;
    #                    ^             ^     ^       ^       ^     ^
    #                    |             |     |       |       |     |
    #                    |             |     |       |       |     +- whitespace before code
    #                    |             |     |       |       +- message text
    #                    |             |     |       +- type (error|warning|note)
    #                    |             |     +- column
    #                    |             +- line
    #                    +- filename
    match = None;
    while ((match = simpleRegex.exec(stdout))):
        messages.push(new Message().fromGcc(match, stdout));

    return messages;


def parseLinker(stdout):
    regex = /(.*):(\d+):\s(.*)\s(to|of)\s`(.*)'/g;

    messages = [];
    match = None;
    while ((match = regex.exec(stdout))):
        messages.push(new Message().fromLinker(match, stdout));

    return messages;
