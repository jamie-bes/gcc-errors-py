(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.GccOutputParser = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

var Message = function Message(components, stdout) {
	if (typeof components[8] === 'undefined') {
		this.filename = components[1];
		this.line = parseInt(components[2]);
		this.column = parseInt(components[3]);
		this.type = components[4];
		this.text = components[5];
		this.codeWhitespace = components[6];
		this.code = components[7];

		this.adjustedColumn = this.column - this.codeWhitespace.length;
		this.startIndex = stdout.indexOf(components[0]);
		this.endIndex = this.startIndex + components[0].length;
	}

	return this;
};

module.exports = Message;

},{}],2:[function(require,module,exports){
'use strict';
var Message = require('./message');

module.exports = {
	parseString: function parseString(stdout) {
		stdout = stdout.toString();
		var regex = /([^:^\n]+):(\d+):(\d+):\s(\w+\s*\w*):\s(.+)\n(\s+)(.*)\s+\^+/gm;
		//            ^          ^     ^       ^       ^     ^    ^
		//            |          |     |       |       |     |    +- affected code
		//            |          |     |       |       |     +- whitespace before code
		//            |          |     |       |       +- message text
		//            |          |     |       +- type (error|warning|note)
		//            |          |     +- column
		//            |          +- line
		//            +- filename

		var messages = [];
		var match = null;
		while (match = regex.exec(stdout)) {
			messages.push(new Message(match, stdout));
		}

		return messages;
	}
};

},{"./message":1}]},{},[2])(2)
});