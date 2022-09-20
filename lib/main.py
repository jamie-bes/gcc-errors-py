// import message

function parseString(stdout) {
    stdout = stdout.toString();

    const messages = [...parseGcc(stdout), ...parseLinker(stdout)];

    return messages;
}

function parseGcc(stdout) {
    const messages = [];
    let match = null;
    const deepRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(\s+)\d*\s*[|]*\s*(.*)\s+[|]*\s*(~*\^~*)/gm;
    //                 ^             ^     ^       ^             ^        ^    |            ^             ^
    //                 |             |     |       |             |        |    |            |             +- token marker
    //                 |             |     |       |             |        |    |            +- affected code
    //                 |             |     |       |             |        |    +- optional gcc 9.2 markup
    //                 |             |     |       |             |        +- whitespace before code
    //                 |             |     |       |             +- message text
    //                 |             |     |       +- type (error|warning|note)
    //                 |             |     +- column
    //                 |             +- line
    //                 +- filename
    while ((match = deepRegex.exec(stdout))) {
        messages.push(new Message().fromGcc(match, stdout));
    }

    const simpleRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(?!\s)/gm;
    //                   ^             ^     ^       ^       ^     ^
    //                   |             |     |       |       |     |
    //                   |             |     |       |       |     +- whitespace before code
    //                   |             |     |       |       +- message text
    //                   |             |     |       +- type (error|warning|note)
    //                   |             |     +- column
    //                   |             +- line
    //                   +- filename
    match = null;
    while ((match = simpleRegex.exec(stdout))) {
        messages.push(new Message().fromGcc(match, stdout));
    }

    return messages;
}

function parseLinker(stdout) {
    const regex = /(.*):(\d+):\s(.*)\s(to|of)\s`(.*)'/g;

    const messages = [];
    let match = null;
    while ((match = regex.exec(stdout))) {
        messages.push(new Message().fromLinker(match, stdout));
    }

    return messages;
}
