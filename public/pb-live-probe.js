/* Prime Books — live file-server probe (shared by amazon.html).
   Mirrors the probe in index.html: tries each known tunnel base, first one
   that answers /library.json becomes __PB_LIVE_BASE.
   If __PB_LIVE_BASES is already defined (e.g. an embedding page or a test
   harness pinning it), respect it and only probe. */
(function () {
  "use strict";
  if (!window.__PB_LIVE_BASES) {
    window.__PB_LIVE_BASES = [
      "https://showcase-polyphonic-tmp-mix.trycloudflare.com",
    ];
  }
  window.__PB_LIVE_BASE = window.__PB_LIVE_BASES[0];
  window.__PB_LIVE = false;
  (function probeLive(i) {
    if (i >= window.__PB_LIVE_BASES.length) return;
    fetch(window.__PB_LIVE_BASES[i] + "/library.json")
      .then(function (r) {
        if (r.ok) {
          window.__PB_LIVE_BASE = window.__PB_LIVE_BASES[i];
          window.__PB_LIVE = true;
        } else probeLive(i + 1);
      })
      .catch(function () { probeLive(i + 1); });
  })(0);
})();
