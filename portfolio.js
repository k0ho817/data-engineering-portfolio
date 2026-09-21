const navToggle = document.querySelector(".nav-toggle");
const navigation = document.getElementById("site-nav");

if (navToggle && navigation) {
  navToggle.addEventListener("click", () => {
    const open = navigation.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.title = open ? "메뉴 닫기" : "메뉴 열기";
  });
  navigation.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navigation.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

const printButton = document.getElementById("print-page");
if (printButton) printButton.addEventListener("click", () => window.print());

const tabs = [...document.querySelectorAll('[role="tab"]')];
function activateTab(tab) {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute("aria-selected", String(selected));
    item.tabIndex = selected ? 0 : -1;
    const panel = document.getElementById(item.getAttribute("aria-controls"));
    if (panel) panel.hidden = !selected;
  });
}

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => activateTab(tab));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
    else if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = tabs.length - 1;
    else return;
    event.preventDefault();
    activateTab(tabs[next]);
    tabs[next].focus();
  });
});

let printState = [];
window.addEventListener("beforeprint", () => {
  printState = [...document.querySelectorAll("details")].map((element) => [
    element,
    element.open,
  ]);
  printState.forEach(([element]) => { element.open = true; });
});
window.addEventListener("afterprint", () => {
  printState.forEach(([element, open]) => { element.open = open; });
});
