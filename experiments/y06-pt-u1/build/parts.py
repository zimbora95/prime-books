"""Shared fragments: icons, chrome, helpers."""

LUPA = '''<svg class="ico" viewBox="0 0 40 40"><circle cx="17" cy="17" r="10.5" fill="#DCE5F0" stroke="#17315A" stroke-width="3.2"/><path d="M12 14.5a6 6 0 0 1 5-4.6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><path d="M25 25l9 9" stroke="#17315A" stroke-width="5" stroke-linecap="round"/></svg>'''
MEGA = '''<svg class="ico" viewBox="0 0 40 40"><path d="M7 16h6l15-8v24l-15-8H7z" fill="#E4502F" stroke="#E4502F" stroke-width="2.4" stroke-linejoin="round"/><path d="M11 24l2.5 8h4.5l-2.2-8" fill="#E4502F"/><path d="M32 14c2 1.6 3 3.6 3 6s-1 4.4-3 6" fill="none" stroke="#E4502F" stroke-width="2.6" stroke-linecap="round"/></svg>'''
PONTE = '''<svg class="ico" viewBox="0 0 40 40"><rect x="2" y="21" width="9" height="12" rx="1.5" fill="#2E8C7B"/><rect x="29" y="21" width="9" height="12" rx="1.5" fill="#2E8C7B"/><path d="M4 22c6-11 26-11 32 0" fill="none" stroke="#2E8C7B" stroke-width="3.2" stroke-linecap="round"/><path d="M11 21h18" stroke="#2E8C7B" stroke-width="2.6"/><path d="M15 21v-4.5M20 21v-6M25 21v-4.5" stroke="#2E8C7B" stroke-width="1.8"/></svg>'''
MICRO = '''<svg class="ico" viewBox="0 0 40 40"><rect x="14" y="4" width="12" height="20" rx="6" fill="#17315A"/><path d="M9 18a11 11 0 0 0 22 0" fill="none" stroke="#17315A" stroke-width="2.8" stroke-linecap="round"/><path d="M20 29v6M13 36h14" stroke="#17315A" stroke-width="2.8" stroke-linecap="round"/></svg>'''
LAPIS = '''<svg class="ico" viewBox="0 0 40 40"><path d="M8 32l3-9L27 7l6 6-16 16z" fill="#F4EDE1" stroke="#17315A" stroke-width="2.6" stroke-linejoin="round"/><path d="M24 10l6 6" stroke="#17315A" stroke-width="2.6"/><path d="M8 32l3-9 6 6z" fill="#E4502F"/></svg>'''

TOTAL = 28
UNIT = {"n": 1, "total": 28}   # a unit module overrides this before building its pages


def qr(key, title, text):
    return f'<div class="qr"><img src="img/{key}.svg" alt="QR"><div class="t"><b>{title}</b>{text}</div></div>'


import os, re
# Book assembly: OFF = the unit's first page in the whole volume minus 1 (always even,
# so left/right parity is unchanged). It shifts the printed folio and every internal
# cross-reference written as "p. N", "pp. N-M", "página N" (all unit-local in the sources).
OFF = int(os.environ.get("OFF", "0") or 0)
_REF = re.compile(r"\b(p\.|pp\.|P\.|PP\.|página|páginas|Página|PÁGINA)(\s?)(\d{1,3})(?:(\s?[–-]\s?)(\d{1,3}))?")


def _shift(m):
    s = f"{m.group(1)}{m.group(2)}{int(m.group(3)) + OFF}"
    if m.group(5):
        s += f"{m.group(4)}{int(m.group(5)) + OFF}"
    return s


def page(n, body, station="", bleed=False, cls="", rh=True, tide=True):
    side = "odd" if n % 2 else "even"
    level = n / UNIT["total"]
    if OFF:
        body = _REF.sub(_shift, body)
    chrome = ""
    if tide:
        on_water = " on-water" if level > 0.9 else ""
        chrome += (f'<div class="tide"><div class="water" style="height:{max(level, 0.075)*100:.1f}%"></div>'
                   f'<div class="station{on_water}">{station}</div>'
                   f'<div class="folio">{n + OFF}</div></div>')
    if rh:
        chrome += (f'<div class="rh"><span class="dot"></span><b>Farol</b> Português 6 · Unidade {UNIT["n"]}'
                   + (f' <span>·</span> {station}' if station else '') + '</div>')
    inner = body if bleed else f'<div class="live">{body}</div>'
    return f'<section class="page {side} u{UNIT['n']} {cls}" data-n="{n}">{inner}{chrome}</section>'


def act(n, verb, html, color=""):
    return (f'<div class="act {color}"><div class="n">{n}</div><div class="q">'
            f'<span class="verb">{verb}</span>{html}</div></div>')


def lines(k):
    return '<div class="lines">' + '<i></i>' * k + '</div>'
