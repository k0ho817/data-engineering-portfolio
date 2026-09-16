const dialog = document.getElementById("image-dialog");
document.querySelectorAll("[data-lightbox]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      event.altKey ||
      !dialog.showModal
    )
      return;
    event.preventDefault();
    const image = link.querySelector("img");
    dialog.querySelector("img").src = link.href;
    dialog.querySelector("img").alt = image.alt;
    document.getElementById("image-title").textContent = link
      .closest("article")
      .querySelector("h3").textContent;
    document.getElementById("image-caption").textContent = link
      .closest("figure")
      .querySelector("figcaption").textContent;
    document.getElementById("image-original").href = link.href;
    dialog.showModal();
  });
});
dialog.addEventListener("click", (event) => {
  const box = dialog.getBoundingClientRect();
  if (
    event.target === dialog &&
    (event.clientX < box.left ||
      event.clientX > box.right ||
      event.clientY < box.top ||
      event.clientY > box.bottom)
  )
    dialog.close();
});
const navigation = [...document.querySelectorAll("nav a")];
const observer = new IntersectionObserver(
  (entries) => {
    const current = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!current) return;
    navigation.forEach((link) => {
      if (link.hash === "#" + current.target.id)
        link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  },
  { rootMargin: "-15% 0px -55% 0px" },
);
document
  .querySelectorAll(".portfolio-section")
  .forEach((section) => observer.observe(section));
let printState = [];
window.addEventListener("beforeprint", () => {
  printState = [...document.querySelectorAll("details")].map((element) => [
    element,
    element.open,
  ]);
  printState.forEach(([element]) => {
    element.open = true;
  });
});
window.addEventListener("afterprint", () =>
  printState.forEach(([element, open]) => {
    element.open = open;
  }),
);
document
  .getElementById("print-page")
  .addEventListener("click", () => window.print());
