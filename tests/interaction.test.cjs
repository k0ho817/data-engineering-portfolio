const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

// Minimal DOM doubles exercise event/state logic without claiming browser QA.
function element(attrs = {}) {
  return {
    attrs, listeners: {}, hidden: false,
    addEventListener(name, handler) { this.listeners[name] = handler; },
    setAttribute(name, value) { this.attrs[name] = value; },
    getAttribute(name) { return this.attrs[name]; },
    focus() { this.focused = true; },
  };
}
const tabs = ["model", "query", "quality"].map(name => element({"aria-controls": `panel-${name}`}));
const ids = {"image-dialog": element(), "print-page": element()};
tabs.forEach(tab => { ids[tab.attrs["aria-controls"]] = element(); });
const details = [{open: false}, {open: true}];
const events = {};
let printed = false;
vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../portfolio.js"), "utf8"), {
  document: {
    getElementById: id => ids[id],
    querySelectorAll: selector => selector === '[role="tab"]' ? tabs : selector === "details" ? details : [],
  },
  window: {addEventListener: (name, fn) => {events[name] = fn;}, print: () => {printed = true;}},
  IntersectionObserver: class { observe() {} },
});
tabs[1].listeners.click();
assert.equal(tabs[1].attrs["aria-selected"], "true");
assert.equal(ids["panel-query"].hidden, false);
assert.equal(ids["panel-model"].hidden, true);
tabs[1].listeners.keydown({key: "End", preventDefault() {}});
assert.equal(tabs[2].attrs["aria-selected"], "true");
tabs[2].listeners.keydown({key: "ArrowRight", preventDefault() {}});
assert.equal(tabs[0].attrs["aria-selected"], "true");
assert.equal(tabs[0].tabIndex, 0);
events.beforeprint();
assert.ok(details.every(item => item.open));
events.afterprint();
assert.equal(details[0].open, false);
assert.equal(details[1].open, true);
ids["print-page"].listeners.click();
assert.ok(printed);
console.log("PASS: SQL tabs, keyboard wrap, print state restoration");
