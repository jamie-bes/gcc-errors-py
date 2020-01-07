'use strict';
var Message = require('./Message');

function parseString(stdout) {
  stdout = stdout.toString();

  var messages = [].concat(parseGcc(stdout), parseLinker(stdout));

  return messages;
}

function parseGcc(stdout) {
  var messages = [];
  var match = null;
  var deepRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(\s+)(.*)\s+(\^~*)/gm;
  //            ^          ^     ^       ^       ^     ^    ^                        ^
  //            |          |     |       |       |     |    +- affected code         +- token marker
  //            |          |     |       |       |     +- whitespace before code
  //            |          |     |       |       +- message text
  //            |          |     |       +- type (error|warning|note)
  //            |          |     +- column
  //            |          +- line
  //            +- filename
  while ((match = deepRegex.exec(stdout))) {
    messages.push(new Message().fromGcc(match, stdout));
  }

  var simpleRegex = /([^:^\r?\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\r?\n(?!\s)/gm;
  //            ^          ^     ^       ^       ^     ^    ^
  //            |          |     |       |       |     |    +- affected code
  //            |          |     |       |       |     +- whitespace before code
  //            |          |     |       |       +- message text
  //            |          |     |       +- type (error|warning|note)
  //            |          |     +- column
  //            |          +- line
  //            +- filename
  match = null;
  while ((match = simpleRegex.exec(stdout))) {
    messages.push(new Message().fromGcc(match, stdout));
  }

  return messages;
}

function parseLinker(stdout) {
  var regex = /(.*):(\d+):\s(.*)\s(to|of)\s`(.*)'/g;

  var messages = [];
  var match = null;
  while ((match = regex.exec(stdout))) {
    messages.push(new Message().fromLinker(match, stdout));
  }

  return messages;
}

module.exports = {
  parseString,
  parseGcc,
  parseLinker
};
