/* Prime Books — live file-server probe (shared by amazon.html).
   Mirrors the probe in index.html: tries each known tunnel base, first one
   that answers /library.json becomes __PB_LIVE_BASE.
   If __PB_LIVE_BASES is already defined (e.g. an embedding page or a test
   harness pinning it), respect it and only probe. */
(function () {
  "use strict";
  if (!window.__PB_LIVE_BASES) {
    window.__PB_LIVE_BASES = [
      "https://methods-museum-quizzes-muscles.trycloudflare.com",
    ];
  }
  window.__PB_LIVE_BASE = window.__PB_LIVE_BASES[0];
  window.__PB_LIVE = false;

  /* Start a cross-origin download IN PLACE.

     A browser ignores an anchor's download attribute when the file comes from
     another origin, and every download these pages offer -- the BookVault text
     and cover files, the KDP wrap covers -- is served by the build server. So a
     plain click opened the browser's reader in a new tab instead of
     downloading. Fetch the bytes and save them here. If the fetch is blocked,
     fall back to the link: the server answers these files with
     Content-Disposition: attachment, which downloads in place even then.

     Call it right after the link is rendered, passing the element, its URL and
     the filename to save as. The anchor's own href/download stay as the
     no-JS fallback. */
  window.pbDownloadLink = function (a, url, name) {
    if (!a) return;
    a.addEventListener("click", function (ev) {
      if (a.dataset.busy === "1" || !window.fetch || !window.URL) return;
      ev.preventDefault();
      var label = a.innerHTML;
      a.dataset.busy = "1";
      a.innerHTML = "&#8681;&nbsp; Preparing&hellip;";
      fetch(url, { cache: "no-store" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.blob();
        })
        .then(function (blob) { saveAs(URL.createObjectURL(blob), true); })
        .catch(function () { saveAs(url, false); })
        .then(function () {
          a.dataset.busy = "";
          a.innerHTML = label;
        });

      function saveAs(href, revoke) {
        var tmp = document.createElement("a");
        tmp.href = href;
        tmp.download = name;
        document.body.appendChild(tmp);
        tmp.click();
        tmp.remove();
        if (revoke) setTimeout(function () { URL.revokeObjectURL(href); }, 60000);
      }
    });
  };

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
