let { Jsonic } = require('jsonic')

let reparse = (s) => {
    try {
        return JSON.stringify(Jsonic(s))
    } catch (e) {
        return e.message.split(/\n/)[0]
    }
}

module.exports = reparse
