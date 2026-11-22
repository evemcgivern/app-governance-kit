// Adds a one-line "Swipe for more" hint above a wide table, shown only while the table overflows.
(function () {
  "use strict";
  function setup(wrap) {
    if (wrap.getAttribute("data-hinted")) { return; }
    wrap.setAttribute("data-hinted", "1");
    var hint = document.createElement("p");
    hint.className = "scroll-hint meta";
    hint.hidden = true;
    hint.setAttribute("aria-hidden", "true");
    hint.textContent = "Swipe for more";
    wrap.parentNode.insertBefore(hint, wrap);
    function update() {
      var over = wrap.scrollWidth > wrap.clientWidth + 1;
      hint.hidden = !over;
    }
    update();
    window.addEventListener("resize", update);
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(update);
      ro.observe(wrap);
      if (wrap.firstElementChild) { ro.observe(wrap.firstElementChild); }
    }
  }
  function scan() {
    [].forEach.call(document.querySelectorAll(".table-scroll, .im-table-wrap"), setup);
  }
  document.addEventListener("DOMContentLoaded", function () {
    scan();
    // Tables the page builds later (the practicum) are picked up as they appear.
    if (window.MutationObserver) {
      new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
    }
  });
})();
