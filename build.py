#!/usr/bin/env python3
"""Rebuild index.html from content/content.json — Benjamin Fehér portfolio.

Usage:
  python3 build.py            # rebuild once
  python3 build.py --watch    # watch content.json; rebuild + commit + push on change
"""
import json, os, subprocess, sys, time

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, 'content', 'content.json')
INDEX = os.path.join(SITE, 'index.html')

MONO = "font-family:var(--mono)"

def read():
    with open(CONTENT) as fh:
        return json.load(fh)

def card(p):
    ph = '<span class="ph">Replace</span>' if p.get('placeholder') else ''
    return (f'<a class="card" href="{p.get("href","#")}">'
            f'<div class="thumb"><span class="fc"></span><span class="glyph">16:9 Frame</span></div>'
            f'<div class="card-top"><span class="card-title">{p["title"]}{ph}</span>'
            f'<span class="card-year">{p["year"]}</span></div>'
            f'<span class="card-meta">{p["meta"]}</span></a>')

def build():
    d = read()
    s, hud = d['site'], d['site']['hud']

    hud_html = (
        f'<div class="hud" aria-hidden="true">'
        f'<div class="hud-top"><div>'
        f'<span>FPS <b>{hud["fps"]}</b></span><span>SHUTTER <b>{hud["shutter"]}</b></span>'
        f'<span>IRIS <b>{hud["iris"]}</b></span><span>EI <b>{hud["ei"]}</b></span><span>ND <b>{hud["nd"]}</b></span>'
        f'</div><div><span>CAM <b>{hud["cam"]}</b></span><span>FCL <b>{hud["fcl"]}</b></span></div></div>'
        f'<div class="hud-bot"><div><span>MEDIA <b>{hud["media"]}</b></span>'
        f'<span class="tc">TC <b id="tc">{hud["tc_start"]}</b></span><span class="live">&#9679; REC</span></div>'
        f'<div><span>A_0004</span><span>C001</span><span>STBY</span></div></div>'
        f'<span class="corner tl"></span><span class="corner tr"></span>'
        f'<span class="corner bl"></span><span class="corner br"></span></div>')

    parts = s['brand'].split('_')
    brand_html = f'{parts[0]}<span>_</span>{parts[1]}' if len(parts) == 2 else s['brand']
    header = (f'<header><a class="brand" href="#top">{brand_html}</a>'
              f'<nav><a href="#work">Work</a><a href="#about">About</a>'
              f'<a href="#contact">Contact</a></nav></header>')

    hero = (f'<section class="hero">'
            f'<p class="hero-kicker mono">{s["role"]}</p>'
            f'<h1 class="hero-name">{s["hero_line1"]}<br><span class="thin">{s["hero_line2"]}</span></h1>'
            f'<p class="hero-sub">{s["tagline"]}</p>'
            f'<a class="reel-cta" href="{s["reel"]["href"]}">'
            f'<span class="playring"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">'
            f'<path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg></span>'
            f'{s["reel"]["label"]} <span class="dur">{s["reel"]["duration"]}</span></a>'
            f'<span class="scroll-cue mono">Scroll &#8595;</span></section>')

    total = sum(len(c['projects']) for c in d['categories'])
    works = (f'<section class="works" id="work">'
             f'<div class="works-head"><h2>Selected Work</h2>'
             f'<span class="count">/ {total} projects</span></div>')
    for c in d['categories']:
        works += (f'<div class="cat" id="{c["id"]}"><div class="cat-head">'
                  f'<h3>{c["title"]} <span>&mdash; {c["count"]}</span></h3>'
                  f'<p>{c["desc"]}</p></div>'
                  f'<div class="grid">{"".join(card(p) for p in c["projects"])}</div></div>')
    works += '</section>'

    a = d['about']
    paras = ''.join(f'<p>{p}</p>' for p in a['paragraphs'])
    about = (f'<section class="about" id="about">'
             f'<div class="about-l">{a["label"]}<span class="loc">{a["loc"]}</span></div>'
             f'<div><p class="about-pull">{a["pull"]}</p>'
             f'<div class="about-body">{paras}</div>'
             f'<p class="clients">{a["collaborators"]}</p></div></section>')

    footer = (f'<footer id="contact">'
              f'<p class="contact-line">{s["contact_line"]}<br>'
              f'<a href="mailto:{s["email"]}">{s["email"]}</a></p>'
              f'<div class="foot-grid"><div class="socials">'
              f'<a href="#">Instagram</a><a href="#">Vimeo</a><a href="#">IMDb</a></div>'
              f'<span class="foot-note">{s["location"]}</span>'
              f'<span class="foot-mono">BF_</span></div></footer>')

    body = hud_html + header + hero + works + about + footer

    with open(INDEX) as fh:
        old = fh.read()
    head = old.split('<body id="top">', 1)[0] + '<body id="top">'
    script = '<script>' + old.split('<script>')[1].split('</script>')[0] + '</script>'
    new = head + '\n' + body + '\n' + script + '\n</body>\n</html>'
    with open(INDEX, 'w') as fh:
        fh.write(new)
    return len(new)

def git(cmd):
    return subprocess.run(cmd, cwd=SITE, capture_output=True, text=True)

def push():
    git(['git', 'add', '-A'])
    r = git(['git', 'commit', '-m', f'content update {time.strftime("%H:%M:%S")}'])
    if 'nothing to commit' in r.stdout + r.stderr:
        return False
    git(['git', 'push'])
    return True

if __name__ == '__main__':
    if '--watch' in sys.argv:
        last = os.path.getmtime(CONTENT)
        print(f'watching {CONTENT}')
        while True:
            time.sleep(2)
            m = os.path.getmtime(CONTENT)
            if m != last:
                last = m
                n = build()
                ok = push()
                print(f'{time.strftime("%H:%M:%S")} rebuilt ({n}B), pushed: {ok}')
    else:
        n = build()
        print(f'index.html rebuilt: {n} bytes')
