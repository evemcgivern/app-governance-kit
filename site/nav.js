// Navigation tooltips: Escape hides the open tip until the pointer or focus moves to another item.
(function () {
  "use strict";
  var nav = document.querySelector(".site-nav");
  if (!nav) { return; }
  function clear() {
    nav.querySelectorAll("li[data-tip-hidden]").forEach(function (li) { li.removeAttribute("data-tip-hidden"); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") { return; }
    nav.querySelectorAll("li:hover, li:focus-within").forEach(function (li) { li.setAttribute("data-tip-hidden", ""); });
  });
  nav.addEventListener("mouseout", clear);
  nav.addEventListener("focusout", clear);
})();

// Footer version: the number comes from version.json, which release-please updates. Without JavaScript
// the link just says "Version" and still leads to the release notes.
(function () {
  "use strict";
  var el = document.getElementById("site-version");
  var script = document.currentScript;
  if (!el || !script || !window.fetch) { return; }
  var base = script.src.replace(/nav\.js.*$/, "");
  fetch(base + "version.json")
    .then(function (r) { return r.json(); })
    .then(function (v) {
      el.textContent = "v" + v.version;
      el.setAttribute("aria-label", "Release notes, version " + v.version);
    })
    .catch(function () { /* keep the plain link */ });
})();
