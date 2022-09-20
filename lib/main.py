import re
from .message import Message

def parseString(stdout):
    assert type(stdout) == str

    messages = [*parseGcc(stdout), *parseLinker(stdout)]

    return messages


def parseGcc(stdout):
    messages = []

    deepRegex = r"([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(\s+)\d*\s*[|]*\s*(.*)\s+[|]*\s*(~*\^~*)"
    #             ^             ^     ^       ^             ^        ^    |            ^             ^
    #             |             |     |       |             |        |    |            |             +- token marker
    #             |             |     |       |             |        |    |            +- affected code
    #             |             |     |       |             |        |    +- optional gcc 9.2 markup
    #             |             |     |       |             |        +- whitespace before code
    #             |             |     |       |             +- message text
    #             |             |     |       +- type (error|warning|note)
    #             |             |     +- column
    #             |             +- line
    #             +- filename
    match = None
    while True:
        match = re.search(deepRegex, stdout, re.MULTILINE)
        if not match:
            break
        messages.append(Message.fromGcc(match, stdout))

    simpleRegex = r"([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(?!\s)"      #gm option?
    #               ^             ^     ^       ^       ^     ^
    #               |             |     |       |       |     |
    #               |             |     |       |       |     +- whitespace before code
    #               |             |     |       |       +- message text
    #               |             |     |       +- type (error|warning|note)
    #               |             |     +- column
    #               |             +- line
    #               +- filename
    match = None
    while True:
        match = re.search(simpleRegex, stdout, re.MULTILINE)
        if not match:
            break
        messages.append(Message.fromGcc(match, stdout))

    return messages


def parseLinker(stdout):
    messages = []

    regex = r"(.*):(\d+):\s(.*)\s(to|of)\s`(.*)'"

    match = None
    while True:
        match = re.search(regex, stdout)
        if not match:
            break
        messages.append(Message.fromLinker(match, stdout))

    return messages
