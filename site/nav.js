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
