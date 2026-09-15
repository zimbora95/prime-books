/* =============================================================================
   Prime Books - per-book URL routing
   =============================================================================
   Gives every book its own address, in the family it belongs to:

       /book/y01-art-and-design              the master, straight from the workshop
       /finished/book/y01-physical-education-standard
                                             the standardised edition, on the
                                             shelf of rebuilt books

   WHY IT MATTERS BEYOND TIDINESS
     The reading assistant keeps ONE Hermes session per book, keyed on the book's
     slug. Making that slug the URL means the address bar, the session and the
     "resume where I left off" behaviour all agree: paste the link to a
     colleague and they land on the same book; reload and you resume the same
     conversation. Without it a book is only reachable by clicking through the
     catalogue, which is also why nobody could bookmark one.

   WHY TWO PREFIXES AND NOT ONE FLAG
     /finished used to be a MODE: the shelf and the reader were one page with a
     flag, and every book opened from inside it pushed a /book/ URL - so a
     refresh dropped the shell and showed the whole book, and the address bar
     said /book/ when the teacher was in fact reading the standard. The mode is
     now in the URL, which is the only thing a reload reads. /finished lists the
     standardised editions; /finished/book/<slug> is one of them.

   HOW IT HOOKS IN
     index.html owns the flipbook. This module never reaches inside it: it waits
     for window.PBLibrary.openSlug (installed by index.html) and calls that.
     Navigation is pushState, so the catalogue does not reload underneath.

   THE ONE SERVER-SIDE REQUIREMENT
     A deep link is a real HTTP request for /book/<slug>, and there is no such
     file. Vite's dev server and Vercel must both rewrite it to /index.html, or
     the first visit 404s while in-app navigation works perfectly - the classic
     SPA trap that only ever shows up on a shared link. See vite.config.js
     (bookDeepLinkFallback) and vercel.json (rewrites). Both must know BOTH
     prefixes, or /finished/book/<slug> 404s on a shared link.
   ============================================================================= */
(function () {
  "use strict";

  var BOOK = "/book/";
  var FINISHED_BOOK = "/finished/book/";
  var FINISHED = "/finished";

  /* Which family the URL we are standing on belongs to. Read from the path, so
     it survives a reload, a bookmark and a link pasted into a fresh tab. */
  function isFinishedPath(pathname) {
    var p = pathname || location.pathname;
    return p === FINISHED || p.indexOf(FINISHED + "/") === 0 || p === FINISHED + ".html";
  }

  function slugFromPath(pathname) {
    var p = pathname || location.pathname;
    var prefix = null;
    if (p.indexOf(FINISHED_BOOK) === 0) prefix = FINISHED_BOOK;
    else if (p.indexOf(BOOK) === 0) prefix = BOOK;
    if (!prefix) return null;
    var slug = p.slice(prefix.length).replace(/\/+$/, "");
    /* Slugs are minted by tools/sync_library.py: lowercase, digits, hyphens.
       Anything else is a hand-typed or hostile URL, not a book. */
    return /^[a-z0-9-]{3,80}$/.test(slug) ? slug : null;
  }

  /* Push a book's URL without reloading. Called by index.html when a flipbook
     opens, so the address bar always names the book on screen - and names it in
     the family of the page it was opened from. */
  function setUrlForSlug(slug, title) {
    if (!slug) return;
    var url = (isFinishedPath() ? FINISHED_BOOK : BOOK) + slug;
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

  /* Return to the shelf the reader came from when a book is closed. */
  function clearUrl() {
    var home = isFinishedPath() ? FINISHED : "/";
    if (location.pathname === home) return;
    try {
      history.pushState({}, "", home);
    } catch (e) {
      return;
    }
    document.title = isFinishedPath() ? "Prime Books \u00b7 the finished shelf" : "Prime Books";
  }

  /* Open whatever book the current URL names. Retries until index.html has
     installed the opener AND the manifest has landed, because a deep link is
     the FIRST thing that happens on a cold load: the catalogue has not been
     built and library.json is still in flight. */
  var pending = null;
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
         a URL that no longer names it. The shelf underneath is already the
         right one - the mode is in the path, and the path is what changed. */
      lib.closeBook();
    }
  });

  window.PBRouter = {
    slugFromPath: slugFromPath,
    setUrlForSlug: setUrlForSlug,
    clearUrl: clearUrl,
    isFinishedPath: isFinishedPath,
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