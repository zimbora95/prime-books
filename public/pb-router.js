/* =============================================================================
   Prime Books - per-book URL routing
   =============================================================================
   Gives every book its own address:

       /book/y01-art-and-design

   WHY IT MATTERS BEYOND TIDINESS
     The reading assistant keeps ONE Hermes session per book, keyed on the book's
     slug. Making that slug the URL means the address bar, the session and the
     "resume where I left off" behaviour all agree: paste the link to a
     colleague and they land on the same book; reload and you resume the same
     conversation. Without it a book is only reachable by clicking through the
     catalogue, which is also why nobody could bookmark one.

   HOW IT HOOKS IN
     index.html owns the flipbook. This module never reaches inside it: it waits
     for window.PBLibrary.openSlug (installed by index.html) and calls that.
     Navigation is pushState, so the catalogue does not reload underneath.

   THE ONE SERVER-SIDE REQUIREMENT
     A deep link is a real HTTP request for /book/<slug>, and there is no such
     file. Vite's dev server and Vercel must both rewrite it to /index.html, or
     the first visit 404s while in-app navigation works perfectly - the classic
     SPA trap that only ever shows up on a shared link. See vite.config.js
     (spaFallback) and vercel.json (rewrites).
   ============================================================================= */
(function () {
  "use strict";

  var PREFIX = "/book/";
  var pending = null;

  function slugFromPath(pathname) {
    var p = pathname || location.pathname;
    if (p.indexOf(PREFIX) !== 0) return null;
    var slug = p.slice(PREFIX.length).replace(/\/+$/, "");
    /* Slugs are minted by tools/sync_library.py: lowercase, digits, hyphens.
       Anything else is a hand-typed or hostile URL, not a book. */
    return /^[a-z0-9-]{3,80}$/.test(slug) ? slug : null;
  }

  /* Push a book's URL without reloading. Called by index.html when a flipbook
     opens, so the address bar always names the book on screen. */
  function setUrlForSlug(slug, title) {
    if (!slug) return;
    var url = PREFIX + slug;
    if (location.pathname === url) return;
    try {
      history.pushState({ slug: slug }, "", url);
    } catch (e) {
      /* file:// or a sandbox with no history access: routing is a bonus here,
         never a hard dependency, so fail quietly and leave the app working. */
      return;
    }
    if (title) document.title = title + " \u00b7 Prime Books";
  }

  /* Return to the catalogue URL when the reader closes a book. */
  function clearUrl() {
    if (location.pathname === "/") return;
    try {
      history.pushState({}, "", "/");
    } catch (e) {
      return;
    }
    document.title = "Prime Books";
  }

  /* Open whatever book the current URL names. Retries until index.html has
     installed the opener AND the manifest has landed, because a deep link is
     the FIRST thing that happens on a cold load: the catalogue has not been
     built and library.json is still in flight. */
  function openFromUrl(attempt) {
    var slug = slugFromPath();
    if (!slug) return;
    var lib = window.PBLibrary;
    if (lib && typeof lib.openSlug === "function") {
      lib.openSlug(slug).then(function (ok) {
        if (!ok && lib.notFound) lib.notFound(slug);
      });
      return;
    }
    if ((attempt || 0) > 60) return; /* ~15 s, then give up silently */
    pending = setTimeout(function () {
      openFromUrl((attempt || 0) + 1);
    }, 250);
  }

  window.addEventListener("popstate", function () {
    var slug = slugFromPath();
    var lib = window.PBLibrary;
    if (!lib) return;
    if (slug) {
      if (typeof lib.openSlug === "function") lib.openSlug(slug);
    } else if (typeof lib.closeBook === "function") {
      /* Back out of a book: close the reader rather than leaving it open over
         a URL that no longer names it. */
      lib.closeBook();
    }
  });

  window.PBRouter = {
    slugFromPath: slugFromPath,
    setUrlForSlug: setUrlForSlug,
    clearUrl: clearUrl,
    openFromUrl: function () {
      if (pending) clearTimeout(pending);
      openFromUrl(0);
    },
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      openFromUrl(0);
    });
  } else {
    openFromUrl(0);
  }
})();
