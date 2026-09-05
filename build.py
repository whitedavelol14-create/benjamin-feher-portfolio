#!/usr/bin/env python3
"""Rebuild index.html from content/content.json — Benjamin Fehér portfolio.

The CSS/JS shell (head, lightbox, timecode, auto-reload) lives here as a
single source; only the body is generated from content.json.

Usage:
  python3 build.py             # rebuild once
  python3 build.py --watch     # watch content.json; rebuild + commit + push on change
"""
import json, os, subprocess, sys, time

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, 'content', 'content.json')
INDEX = os.path.join(SITE, 'index.html')

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Benjamin Fehér — Director & Cinematographer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0c0d0f;--panel:#121417;--ink:#e8e6e1;--dim:#8a8f98;--faint:#4c5158;
    --line:rgba(255,255,255,.08);--rec:#c33;
    --sans:'Space Grotesk',system-ui,-apple-system,sans-serif;
    --mono:'IBM Plex Mono','SF Mono',monospace;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
  ::selection{background:var(--rec);color:#fff}
  a{color:inherit;text-decoration:none}
  :focus-visible{outline:2px solid var(--rec);outline-offset:3px}
  .mono{font-family:var(--mono)}

  /*= HUD =*/
  .hud{position:fixed;inset:0;pointer-events:none;z-index:40;font-family:var(--mono);font-size:.58rem;letter-spacing:.08em;color:var(--dim);text-transform:uppercase}
  .hud-top{position:absolute;top:.9rem;left:1.2rem;right:1.2rem;display:flex;justify-content:space-between;gap:1rem}
  .hud-bot{position:absolute;bottom:.9rem;left:1.2rem;right:1.2rem;display:flex;justify-content:space-between;gap:1rem}
  .hud-top>div,.hud-bot>div{display:flex;gap:1.6rem;flex-wrap:wrap}
  .hud b{color:var(--ink);font-weight:500}
  .hud .live{color:var(--rec);animation:rec 1.6s steps(1,end) infinite}
  @keyframes rec{0%,55%{opacity:1}56%,100%{opacity:.2}}
  .hud .tc b{font-variant-numeric:tabular-nums}
  .corner{position:fixed;width:14px;height:14px;z-index:40;pointer-events:none;border-color:var(--faint);border-style:solid;border-width:0}
  .corner.tl{top:10px;left:10px;border-top-width:1px;border-left-width:1px}
  .corner.tr{top:10px;right:10px;border-top-width:1px;border-right-width:1px}
  .corner.bl{bottom:10px;left:10px;border-bottom-width:1px;border-left-width:1px}
  .corner.br{bottom:10px;right:10px;border-bottom-width:1px;border-right-width:1px}

  /*= header =*/
  header{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;justify-content:space-between;align-items:center;padding:1rem clamp(1.25rem,4vw,2.6rem);background:linear-gradient(to bottom,rgba(12,13,15,.92),rgba(12,13,15,0))}
  .brand{font-family:var(--mono);font-size:.72rem;letter-spacing:.2em}
  .brand span{color:var(--rec)}
  nav{display:flex;gap:1.8rem}
  nav a{font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);transition:color .2s}
  nav a:hover{color:var(--ink)}

  /*= hero =*/
  .hero{min-height:100vh;position:relative;display:flex;flex-direction:column;justify-content:flex-end;padding:0 clamp(1.25rem,4vw,2.6rem) 7rem;background:radial-gradient(ellipse 120% 70% at 50% 108%,rgba(195,51,51,.06),transparent 55%),radial-gradient(ellipse 80% 60% at 85% -10%,rgba(232,230,225,.05),transparent 60%),var(--bg)}
  .hero-kicker{font-family:var(--mono);color:var(--dim);margin-bottom:1.2rem}
  .hero-name{font-size:clamp(3.6rem,10.5vw,10rem);font-weight:500;line-height:.96;letter-spacing:-.02em}
  .hero-name .thin{color:var(--dim)}
  .hero-sub{max-width:33rem;margin-top:1.8rem;color:var(--dim);font-size:1rem}
  .hero-sub strong{color:var(--ink);font-weight:500}
  .reel-cta{position:absolute;bottom:7rem;right:clamp(1.25rem,4vw,2.6rem);display:flex;align-items:center;gap:1rem;font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase}
  .reel-cta .playring{width:52px;height:52px;border-radius:50%;border:1px solid var(--faint);display:grid;place-items:center;transition:border-color .25s,transform .25s}
  .reel-cta:hover .playring{border-color:var(--rec);transform:scale(1.06)}
  .reel-cta svg{margin-left:3px}
  .reel-cta .dur{color:var(--faint)}
  .scroll-cue{position:absolute;bottom:2rem;left:clamp(1.25rem,4vw,2.6rem);color:var(--faint);font-family:var(--mono);font-size:.6rem;letter-spacing:.14em;text-transform:uppercase}

  /*= works =*/
  .works{padding:6rem clamp(1.25rem,4vw,2.6rem) 4rem}
  .works-head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:1.1rem;margin-bottom:.4rem}
  .works-head h2{font-family:var(--mono);font-weight:400;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
  .works-head .count{font-family:var(--mono);font-size:.6rem;color:var(--faint)}
  .cat{margin-top:4.5rem}
  .cat-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1.2rem}
  .cat-head h3{font-family:var(--mono);font-weight:400;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase}
  .cat-head h3 span{color:var(--rec)}
  .cat-head p{font-family:var(--mono);font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
  .card{background:var(--bg);padding:1.1rem 1.1rem 1.4rem;display:flex;flex-direction:column;gap:.8rem;border:1px solid var(--line);cursor:pointer;transition:background .25s}
  .card:hover{background:#14161a}
  .thumb{aspect-ratio:16/9;background:var(--panel);display:grid;place-items:center;overflow:hidden;border:1px solid var(--line);position:relative}
  .thumb .glyph{font-family:var(--mono);font-size:.6rem;letter-spacing:.14em;color:var(--faint);text-transform:uppercase}
  .fc{position:absolute;inset:0;pointer-events:none}
  .fc::before,.fc::after{content:'';position:absolute;width:10px;height:10px;border-color:var(--faint);border-style:solid;border-width:0;transition:border-color .25s}
  .fc::before{top:8px;left:8px;border-top-width:1px;border-left-width:1px}
  .fc::after{bottom:8px;right:8px;border-bottom-width:1px;border-right-width:1px}
  .card:hover .fc::before,.card:hover .fc::after{border-color:var(--dim)}
  .card:hover .thumb .glyph{color:var(--dim)}
  .card-top{display:flex;justify-content:space-between;align-items:baseline;gap:1rem}
  .card-title{font-size:1.05rem;font-weight:500;letter-spacing:-.01em}
  .card-title .ph{display:inline-block;font-family:var(--mono);font-size:.52rem;letter-spacing:.12em;text-transform:uppercase;color:var(--rec);border:1px solid rgba(195,51,51,.5);border-radius:2px;padding:.12rem .4rem;margin-left:.6rem;vertical-align:2px}
  .card-year{font-family:var(--mono);font-size:.6rem;color:var(--faint)}
  .card-meta{font-family:var(--mono);font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
  .card .thumb .play{position:absolute;inset:0;display:grid;place-items:center;opacity:0;transition:opacity .25s}
  .card:hover .thumb .play{opacity:1}
  .play-badge{width:44px;height:44px;border-radius:50%;border:1px solid var(--ink);display:grid;place-items:center;background:rgba(12,13,15,.55)}
  .play-badge svg{margin-left:3px}

  /*= about =*/
  .about{border-top:1px solid var(--line);padding:7rem clamp(1.25rem,4vw,2.6rem);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:4rem}
  .about-l{font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
  .about-l .loc{display:block;margin-top:.8rem;color:var(--faint)}
  .about-pull{font-size:clamp(1.5rem,2.8vw,2.3rem);font-weight:400;line-height:1.3;letter-spacing:-.01em;max-width:44rem;margin-bottom:2.2rem}
  .about-pull em{font-style:normal;color:var(--dim)}
  .about-body{color:var(--dim);max-width:38rem}
  .about-body p+p{margin-top:1rem}
  .about-body strong{color:var(--ink);font-weight:500}
  .clients{margin-top:2.4rem;font-family:var(--mono);font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}

  /*= footer =*/
  footer{border-top:1px solid var(--line);padding:4.5rem clamp(1.25rem,4vw,2.6rem) 2.2rem}
  .contact-line{font-size:clamp(2rem,5vw,4.2rem);font-weight:500;letter-spacing:-.02em;line-height:1.05;margin-bottom:3.2rem}
  .contact-line a{border-bottom:2px solid var(--rec);transition:color .2s}
  .contact-line a:hover{color:var(--rec)}
  .foot-grid{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:1.6rem}
  .socials{display:flex;gap:1.8rem;font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;text-transform:uppercase}
  .socials a{color:var(--dim);transition:color .2s}
  .socials a:hover{color:var(--ink)}
  .foot-note{font-family:var(--mono);font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
  .foot-mono{font-family:var(--mono);font-size:1.6rem;color:var(--faint)}

  /*= lightbox =*/
  .lb{position:fixed;inset:0;z-index:100;background:rgba(5,5,6,.92);display:none;align-items:center;justify-content:center;padding:2rem}
  .lb.open{display:flex}
  .lb-frame{position:relative;width:min(1000px,92vw);aspect-ratio:16/9;background:#000;box-shadow:0 20px 80px rgba(0,0,0,.6)}
  .lb-frame.portrait{width:auto;height:min(80vh,92vw);aspect-ratio:9/16}
  .lb-frame iframe{width:100%;height:100%;border:0;display:block}
  .lb-close{position:absolute;top:-2.6rem;right:0;background:none;border:none;color:#e8e6e1;font-size:2rem;cursor:pointer;line-height:1}

  @media(max-width:760px){
    nav{display:none}
    .cat-head{flex-direction:column;align-items:flex-start;gap:.4rem}
    .reel-cta{display:none}
  }
</style>
</head>
<body id="top">
"""

TAIL = """
<!-- lightbox -->
<div class="lb" id="lb" role="dialog" aria-label="Video player">
  <div class="lb-frame">
    <button class="lb-close" id="lb-close" aria-label="Close">&times;</button>
    <iframe id="lb-iframe" src="" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>
  </div>
</div>
<script>
  // live timecode (24fps, runs from 02:20:35:09)
  (function(){
    var el = document.getElementById('tc');
    if(!el) return;
    var baseFrames = ((2*3600 + 20*60 + 35) * 24) + 9;
    var t0 = performance.now();
    function pad(n){ return String(n).padStart(2,'0'); }
    function tick(){
      var total = baseFrames + Math.floor((performance.now() - t0) / 1000 * 24);
      var f = total % 24; total = Math.floor(total / 24);
      var s = total % 60; total = Math.floor(total / 60);
      var m = total % 60; total = Math.floor(total / 60);
      el.textContent = pad(total % 24) + ':' + pad(m) + ':' + pad(s) + ':' + pad(f);
    }
    setInterval(tick, 1000 / 12);
    tick();
  })();

  // video lightbox (YouTube + Instagram Reels)
  (function(){
    function resolveEmbed(src){
      if(!src) return null;
      src = src.trim();
      if(!src) return null;
      var u;
      try { u = new URL(/^https?:/i.test(src) ? src : 'https://' + src); } catch(e){ return null; }
      // YouTube
      if(/(^|\.)youtube\.com$/.test(u.hostname) || /(^|\.)youtu\.be$/.test(u.hostname)){
        var m = (u.searchParams && u.searchParams.get('v')) || (u.pathname.match(/\/(watch|embed|shorts)\/([\w-]{11})/) && u.pathname.match(/\/(watch|embed|shorts)\/([\w-]{11})/)[2]);
        if(!m && u.pathname.indexOf('youtu.be') !== -1){ m = u.pathname.slice(1).split('/')[0]; }
        if(!m && /^[\w-]{11}$/.test(src)){ m = src; }
        return m ? {src: 'https://www.youtube.com/embed/' + m + '?autoplay=1&rel=0', portrait:false} : null;
      }
      // Instagram (reel or post)
      if(u.hostname.indexOf('instagram.com') !== -1){
        var r = u.pathname.match(/\/(reel|p|tv)\/([A-Za-z0-9_-]+)/);
        return r ? {src: 'https://www.instagram.com/' + r[1] + '/' + r[2] + '/embed', portrait:true} : null;
      }
      // raw instagram shortcode
      if(/^[A-Za-z0-9_-]{8,}$/.test(src) && src.length < 25){ return {src:'https://www.instagram.com/reel/' + src + '/embed', portrait:true}; }
      // Vimeo
      if(u.hostname.indexOf('vimeo.com') !== -1){
        var vm = u.pathname.match(/\/video\/(\d+)/) || u.pathname.match(/^\/(\d+)/);
        return vm ? {src:'https://player.vimeo.com/video/' + vm[1] + '?autoplay=1', portrait:false} : null;
      }
      return null;
    }
    var lb = document.getElementById('lb');
    var ifr = document.getElementById('lb-iframe');
    var frame = document.querySelector('.lb-frame');
    var close = document.getElementById('lb-close');
    function closeLb(){
      lb.classList.remove('open');
      frame.classList.remove('portrait');
      ifr.src = '';
    }
    close.addEventListener('click', closeLb);
    lb.addEventListener('click', function(e){ if(e.target === lb) closeLb(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeLb(); });
    document.querySelectorAll('.card[data-video]').forEach(function(card){
      card.addEventListener('click', function(e){
        var emb = resolveEmbed(card.getAttribute('data-video'));
        if(!emb) return;
        e.preventDefault();
        frame.classList.toggle('portrait', !!emb.portrait);
        ifr.src = emb.src;
        lb.classList.add('open');
      });
    });
  })();

  // local preview auto-reload (harmless on GitHub Pages: build-timestamp.txt 404s)
  (function(){var last=null;setInterval(function(){fetch('build-timestamp.txt?t='+Date.now()).then(function(r){return r.ok?r.text():null}).then(function(t){if(t && last!==null && t!==last){location.reload();}if(t){last=t;}}).catch(function(){});},2500);})();
</script>
</body>
</html>
"""

MONO = "font-family:var(--mono)"

def read():
    with open(CONTENT) as fh:
        return json.load(fh)

def card(p, ci):
    ph = '<span class="ph">Replace</span>' if p.get('placeholder') else ''
    vid = p.get('video', '') or ''
    dv = f'data-video="{vid}"' if vid else ''
    play = ''
    if vid:
        play = ('<span class="play"><span class="play-badge">'
                '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z" fill="currentColor"/></svg>'
                '</span></span>')
    return (f'<a class="card" {dv} href="{p.get("href","#")}">'
            f'<div class="thumb"><span class="fc"></span><span class="glyph">16:9 Frame</span>{play}</div>'
            f'<div class="card-top"><span class="card-title"{ed(ci+".title")}>{p["title"]}{ph}</span>'
            f'<span class="card-year"{ed(ci+".year")}>{p["year"]}</span></div>'
            f'<span class="card-meta"{ed(ci+".meta")}>{p["meta"]}</span></a>')

def ed(path):
    return f' data-edit="{path}"'

def build():
    d = read()
    s, hud = d['site'], d['site']['hud']

    hud_html = (
        f'<div class="hud" aria-hidden="true">'
        f'<div class="hud-top"><div><span>FPS <b>{hud["fps"]}</b></span>'
        f'<span>SHUTTER <b>{hud["shutter"]}</b></span><span>IRIS <b>{hud["iris"]}</b></span>'
        f'<span>EI <b>{hud["ei"]}</b></span><span>ND <b>{hud["nd"]}</b></span></div>'
        f'<div><span>CAM <b>{hud["cam"]}</b></span><span>FCL <b>{hud["fcl"]}</b></span></div></div>'
        f'<div class="hud-bot"><div><span>MEDIA <b>{hud["media"]}</b></span>'
        f'<span class="tc">TC <b id="tc">{hud["tc_start"]}</b></span>'
        f'<span class="live">&#9679; REC</span></div>'
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
    for ci2, c in enumerate(d['categories']):
        cards = ''.join(card(p, f"categories.{ci2}.projects.{i}") for i, p in enumerate(c['projects']))
        works += (f'<div class="cat" id="{c["id"]}"><div class="cat-head">'
                  f'<h3>{c["title"]} <span>&mdash; {c["count"]}</span></h3>'
                  f'<p>{c["desc"]}</p></div>'
                  f'<div class="grid">{cards}</div></div>')
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
    new = HEAD + body + TAIL
    with open(INDEX, 'w') as fh:
        fh.write(new)
    with open(os.path.join(SITE, 'build-timestamp.txt'), 'w') as fh:
        fh.write(str(time.time()))
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