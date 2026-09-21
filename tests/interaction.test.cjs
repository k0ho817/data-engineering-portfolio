const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function element(attrs = {}) {
  return {
    attrs, listeners: {}, hidden: false, open: false,
    classList: {
      values: new Set(),
      toggle(value) {
        if (this.values.has(value)) { this.values.delete(value); return false; }
        this.values.add(value); return true;
      },
      remove(value) { this.values.delete(value); },
    },
    addEventListener(name, handler) { this.listeners[name] = handler; },
    setAttribute(name, value) { this.attrs[name] = value; },
    getAttribute(name) { return this.attrs[name]; },
    querySelectorAll() { return []; },
    focus() { this.focused = true; },
  };
}

const tabs = ["model", "query", "quality"].map(name => element({"aria-controls": "panel-" + name}));
const navigation = element();
const navLink = element();
navigation.querySelectorAll = () => [navLink];
const navToggle = element();
const printButton = element();
const ids = {"site-nav": navigation, "print-page": printButton};
tabs.forEach(tab => { ids[tab.attrs["aria-controls"]] = element(); });
const details = [element(), element()];
details[1].open = true;
const events = {};
let printed = false;

vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../portfolio.js"), "utf8"), {
  document: {
    querySelector: selector => selector === ".nav-toggle" ? navToggle : null,
    getElementById: id => ids[id] || null,
    querySelectorAll: selector => selector === '[role="tab"]' ? tabs : selector === "details" ? details : [],
  },
  window: {addEventListener: (name, fn) => { events[name] = fn; }, print: () => { printed = true; }},
});

navToggle.listeners.click();
assert.equal(navToggle.attrs["aria-expanded"], "true");
navLink.listeners.click();
assert.equal(navToggle.attrs["aria-expanded"], "false");
tabs[1].listeners.click();
assert.equal(tabs[1].attrs["aria-selected"], "true");
assert.equal(ids["panel-query"].hidden, false);
tabs[1].listeners.keydown({key: "End", preventDefault() {}});
assert.equal(tabs[2].attrs["aria-selected"], "true");
tabs[2].listeners.keydown({key: "ArrowRight", preventDefault() {}});
assert.equal(tabs[0].attrs["aria-selected"], "true");
events.beforeprint();
assert.ok(details.every(item => item.open));
events.afterprint();
assert.equal(details[0].open, false);
assert.equal(details[1].open, true);
printButton.listeners.click();
assert.ok(printed);
console.log("PASS: mobile navigation, SQL tabs and print state");
