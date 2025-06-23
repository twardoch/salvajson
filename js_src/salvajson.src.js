let { Jsonic } = require("jsonic");

let reparse = (s) => {
  try {
    // Ensure Jsonic output is an object/array before stringifying,
    // as Jsonic can return primitive types for certain inputs (e.g. "123").
    const parsed = Jsonic(s);
    // Check if Jsonic itself failed and returned an error object
    // (Jsonic's own error handling can be a bit peculiar depending on options)
    if (parsed instanceof Error) {
      throw parsed;
    }
    return JSON.stringify(parsed);
  } catch (e) {
    // Re-throw the error so pythonmonkey can catch it
    throw e;
  }
};

module.exports = reparse;
