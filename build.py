#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py, générateur de la veille créative de Karl Petzold.

Usage :
    python3 build.py data-AAAA-MM-JJ.json ./
    python3 build.py data-AAAA-MM-JJ.json ./ --images=inline

Produit :
    veille-AAAA-MM-JJ.html   la page de l'édition demandée
    index.html               l'accueil, régénéré à partir de tous les data*.json du dossier
    artefact-AAAA-MM-JJ.html uniquement avec --images=inline (images embarquées en data URI)

Schémas de data acceptés :
    courant    { "date", "meta": {...}, "intro", "entrees": [ { "rubrique", ... } ] }
    historique { "date_iso", "chapeau", "categories": [ { "id", "items": [...] } ] }
Un meta-AAAA-MM-JJ.json à côté du data est lu s'il existe et complète la clé "meta".
"""

import base64
import html
import json
import os
import re
import sys
from datetime import date

# --------------------------------------------------------------------------
# Rubriques : ordre, libellé, couleur d'accent
# --------------------------------------------------------------------------

RUBRIQUES = [
    ("direction-artistique", "Direction artistique & campagnes", "#c9a24a"),
    ("mode",                 "Mode",                             "#a3ad72"),
    ("luxe",                 "Luxe",                             "#b57a8c"),
    ("craft",                "Craft & matière",                  "#b8956a"),
    ("architecture",         "Architecture",                     "#8d9aa3"),
    ("scenographie",         "Scénographie & expérience",        "#7fbdb0"),
    ("photographie",         "Photographie",                     "#6fa3bd"),
    ("film",                 "Film & motion",                    "#c47a72"),
    ("fantasy",              "Fantasy art & illustration",       "#9b7ec9"),
    ("gaming",               "Gaming & worldbuilding",           "#cd8659"),
    ("ui",                   "UI & design d'interface",          "#8592c9"),
    ("ia",                   "IA & création",                    "#6fbd97"),
    ("philosophie",          "Philosophie",                       "#a8a196"),
]
ORDER = {rid: i for i, (rid, _, _) in enumerate(RUBRIQUES)}
LABEL = {rid: lab for rid, lab, _ in RUBRIQUES}
ACCENT = {rid: acc for rid, _, acc in RUBRIQUES}

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

ACCENT_GLOBAL = "#D9FF3D"

# --------------------------------------------------------------------------
# Lecture des données
# --------------------------------------------------------------------------


def date_longue(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    dt = date(y, m, d)
    return "%s %d %s %d" % (JOURS[dt.weekday()], d, MOIS[m - 1], y)


def date_courte(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%02d.%02d.%d" % (d, m, y)


def deviner_date(chemin, brut):
    for cle in ("date", "date_iso"):
        v = brut.get(cle)
        if isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            return v
    nom = os.path.basename(chemin)
    m = re.search(r"(\d{4})-?(\d{2})-?(\d{2})", nom)
    if m:
        return "%s-%s-%s" % m.groups()
    return None


def normaliser(chemin):
    """Renvoie un dict homogène : date, meta, intro, entrees."""
    with open(chemin, "r", encoding="utf-8") as f:
        brut = json.load(f)

    iso = deviner_date(chemin, brut)
    if not iso:
        return None

    meta = dict(brut.get("meta") or {})
    voisin = os.path.join(os.path.dirname(chemin) or ".", "meta-%s.json" % iso)
    if os.path.exists(voisin):
        try:
            with open(voisin, "r", encoding="utf-8") as f:
                meta.update(json.load(f) or {})
        except (ValueError, OSError):
            pass

    entrees = []
    if isinstance(brut.get("entrees"), list):
        entrees = list(brut["entrees"])
    elif isinstance(brut.get("categories"), list):
        for cat in brut["categories"]:
            rid = cat.get("id") or cat.get("rubrique")
            for item in cat.get("items") or []:
                e = dict(item)
                e.setdefault("rubrique", rid)
                entrees.append(e)

    propres = []
    for e in entrees:
        rid = e.get("rubrique") or e.get("id")
        if rid not in ORDER:
            continue
        imgs = [u for u in (e.get("images") or []) if isinstance(u, str) and u.strip()]
        propres.append({
            "rubrique": rid,
            "titre": e.get("titre") or e.get("title") or "",
            "type": (e.get("type") or "actualite").lower(),
            "source_nom": e.get("source_nom") or e.get("source") or "",
            "source_url": e.get("source_url") or e.get("url") or "",
            "images": imgs[:3],
            "contexte_html": e.get("contexte_html") or e.get("contexte") or "",
            "learning": e.get("learning") or "",
        })
    propres.sort(key=lambda e: ORDER[e["rubrique"]])

    return {
        "fichier": chemin,
        "date": iso,
        "meta": meta,
        "intro": brut.get("intro") or brut.get("chapeau") or "",
        "entrees": propres,
    }


def charger_editions(dossier):
    editions = []
    for nom in sorted(os.listdir(dossier)):
        if not nom.startswith("data") or not nom.endswith(".json"):
            continue
        ed = normaliser(os.path.join(dossier, nom))
        if ed and ed["entrees"]:
            editions.append(ed)

    # Éditions antérieures dont le data n'est pas dans ce dossier : gardées pour
    # la numérotation et l'archive. Un vrai data-AAAA-MM-JJ.json a toujours priorité.
    connues = {e["date"] for e in editions}
    passees = os.path.join(dossier, "editions-passees.json")
    if os.path.exists(passees):
        try:
            with open(passees, "r", encoding="utf-8") as f:
                for row in json.load(f) or []:
                    iso = (row or {}).get("date")
                    if not iso or iso in connues:
                        continue
                    connues.add(iso)
                    editions.append({
                        "fichier": passees, "date": iso, "stub": True,
                        "meta": {k: v for k, v in row.items() if k != "date"},
                        "intro": "", "entrees": [],
                    })
        except (ValueError, OSError):
            pass

    editions.sort(key=lambda e: e["date"])
    vus = set()
    uniques = []
    for ed in editions:                      # une seule édition par date
        if ed["date"] in vus:
            continue
        vus.add(ed["date"])
        uniques.append(ed)
    for i, ed in enumerate(uniques, start=1):  # numérotation recalculée
        ed["numero"] = i
    return uniques


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------

def inliner(url, cache):
    """Télécharge une image et la renvoie en data URI. Rend l'URL telle quelle en cas d'échec."""
    if url in cache:
        return cache[url]
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
            ctype = r.headers.get_content_type() or "image/jpeg"
        if len(data) > 4_500_000:
            raise ValueError("image trop lourde")
        uri = "data:%s;base64,%s" % (ctype, base64.b64encode(data).decode("ascii"))
    except Exception as exc:                                    # noqa: BLE001
        sys.stderr.write("  image non embarquée (%s) : %s\n" % (exc, url))
        uri = url
    cache[url] = uri
    return uri


def resoudre_images(urls, mode, cache):
    if mode != "inline":
        return list(urls)
    return [inliner(u, cache) for u in urls]


# --------------------------------------------------------------------------
# Gabarits
# --------------------------------------------------------------------------

GRAIN = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
    "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/>"
    "<feColorMatrix type='saturate' values='0'/></filter>"
    "<rect width='240' height='240' filter='url(%23n)' opacity='0.5'/></svg>"
)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Unbounded:wght@400;600;800;900&'
    'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

BASE_CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0a0a0b; --bg-2:#111113; --ink:#f4f4f0; --muted:#8b8b85;
  --line:rgba(255,255,255,.13); --accent:%(accent)s;
  --serif:'Unbounded','Outfit','Helvetica Neue',sans-serif;
  --sans:'Inter','Helvetica Neue',Arial,sans-serif;
  --pad:clamp(20px,5vw,72px);
}
html{-webkit-text-size-adjust:100%%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-weight:500;font-size:15px;line-height:1.62;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
img{max-width:100%%;display:block}
a{color:inherit}
::selection{background:var(--accent);color:#000}
.kicker{font-size:10.5px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.grain{position:fixed;inset:0;pointer-events:none;z-index:60;opacity:.05;
  background-image:url("%(grain)s");background-size:240px;mix-blend-mode:overlay}
.bar{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;
  justify-content:space-between;gap:16px;padding:14px var(--pad);
  background:linear-gradient(to bottom,rgba(10,10,11,.92),rgba(10,10,11,0));
  backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px)}
.bar__id{font-size:10.5px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
  color:var(--ink);text-decoration:none;opacity:.85;transition:opacity .3s}
.bar__id:hover{opacity:1}
.btn{display:inline-block;font-size:10px;font-weight:600;letter-spacing:.2em;
  text-transform:uppercase;text-decoration:none;padding:9px 15px;border-radius:2px;
  border:1px solid var(--accent);color:var(--accent);
  background:color-mix(in srgb,var(--accent) 30%%,transparent);
  transition:background .35s ease,color .35s ease,transform .35s ease}
.btn:hover{background:var(--accent);color:#0a0a0b;transform:translateY(-1px)}
.progress{position:fixed;top:0;left:0;height:2px;width:0;background:var(--accent);z-index:70;
  transition:width .12s linear}
.hide-s{display:inline}
footer{padding:clamp(48px,9vh,104px) var(--pad);border-top:1px solid var(--line);
  display:flex;flex-wrap:wrap;gap:14px 26px;justify-content:space-between;align-items:center}
@media (max-width:680px){
  .hide-s{display:none}
  .bar{padding:11px 16px}
  .bar__id{font-size:9.5px;letter-spacing:.14em}
  .btn{padding:8px 11px;font-size:9px;letter-spacing:.13em;white-space:nowrap}
}
.reveal{opacity:0;transform:translateY(26px);
  transition:opacity 1s cubic-bezier(.22,.7,.24,1),transform 1s cubic-bezier(.22,.7,.24,1)}
.reveal.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .reveal{opacity:1;transform:none;transition:none}
}
"""

EDITION_CSS = """
main{scroll-snap-type:y proximity}
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;
  padding:0 var(--pad) clamp(38px,7vh,86px);overflow:hidden;scroll-snap-align:start}
.hero__img{position:absolute;inset:0;z-index:0}
.hero__img img{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.16) brightness(.62);
  transform:scale(1.06);animation:drift 22s ease-out forwards}
@keyframes drift{to{transform:scale(1)}}
.hero__veil{position:absolute;inset:0;z-index:1;
  background:radial-gradient(120% 90% at 20% 100%,rgba(10,10,11,.35),rgba(10,10,11,.94) 72%),
             linear-gradient(to top,rgba(10,10,11,.98),rgba(10,10,11,.2) 55%,rgba(10,10,11,.72))}
.hero__in{position:relative;z-index:2;max-width:1180px;width:100%}
.hero__no{font-family:var(--serif);font-weight:800;font-size:11px;letter-spacing:.32em;
  color:var(--accent);margin:0 0 18px}
.hero h1{font-family:var(--serif);font-weight:900;letter-spacing:-.02em;line-height:.92;
  font-size:clamp(38px,8.2vw,116px);margin:0 0 22px;text-transform:uppercase}
.hero__meta{display:flex;flex-wrap:wrap;gap:10px 22px;margin-bottom:22px}
.hero__deck{max-width:62ch;font-size:15px;color:#cfcfc8;margin:0}
.hero__scroll{position:absolute;left:var(--pad);bottom:14px;z-index:2;font-size:9.5px;
  letter-spacing:.24em;text-transform:uppercase;color:var(--muted);animation:blink 3.2s infinite}
@keyframes blink{0%,100%{opacity:.35}50%{opacity:.9}}

.sommaire{padding:clamp(64px,12vh,140px) var(--pad);border-top:1px solid var(--line);
  scroll-snap-align:start}
.sommaire__in{max-width:1180px;margin:0 auto}
.sommaire p.intro{font-size:clamp(17px,2.1vw,25px);line-height:1.42;max-width:32ch;
  font-family:var(--serif);font-weight:400;margin:18px 0 clamp(38px,6vh,64px)}
.som__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  column-gap:clamp(24px,5vw,80px)}
.som__row{display:flex;gap:14px;align-items:baseline;padding:11px 0;border-top:1px solid var(--line);
  text-decoration:none;transition:padding-left .35s ease}
.som__row:hover{padding-left:8px}
.som__n{font-family:var(--serif);font-size:10px;font-weight:600;color:var(--muted);min-width:22px}
.som__t{font-size:14px;font-weight:500;flex:1}
.som__r{font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);
  text-align:right;white-space:nowrap}
.som__row:hover .som__t{color:var(--accent)}

.entry{min-height:100svh;display:grid;align-items:center;
  grid-template-columns:minmax(0,.86fr) minmax(0,1fr);
  gap:clamp(28px,4.5vw,74px);padding:clamp(72px,11vh,124px) var(--pad);
  border-top:1px solid var(--line);scroll-snap-align:start}
.media{display:grid;gap:8px;width:100%;aspect-ratio:3/4;max-height:78vh;margin:0 auto}
.media--1{grid-template-rows:1fr}
.media--2{grid-template-rows:1.75fr 1fr}
.media--3{grid-template-rows:1.75fr 1fr;grid-template-columns:1fr 1fr}
.media--3 .shot:first-child{grid-column:1 / -1}
.shot{position:relative;overflow:hidden;background:var(--bg-2)}
.shot img{width:100%;height:100%;object-fit:cover;transform:scale(1.03);
  transition:transform 1.4s cubic-bezier(.22,.7,.24,1)}
.shot:hover img{transform:scale(1.08)}
.txt{max-width:56ch}
.tag{display:flex;align-items:center;gap:10px;margin-bottom:20px;flex-wrap:wrap}
.dot{width:7px;height:7px;border-radius:50%;background:var(--rc)}
.tag__r{font-size:10px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--rc)}
.tag__n{font-family:var(--serif);font-size:10px;font-weight:600;color:var(--muted);margin-left:auto}
.pepite{font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
  color:#0a0a0b;background:var(--rc);padding:3px 8px;border-radius:2px}
.entry h2{font-family:var(--serif);font-weight:800;letter-spacing:-.015em;line-height:1.08;
  font-size:clamp(23px,2.9vw,40px);margin:0 0 22px}
.ctx{font-size:15px;line-height:1.68;color:#d6d6d0;margin:0 0 26px}
.ctx a{color:var(--ink);text-decoration:none;background-image:linear-gradient(var(--rc),var(--rc));
  background-size:100% 1px;background-repeat:no-repeat;background-position:0 100%;
  padding-bottom:1px;transition:background-size .4s ease,color .3s ease}
.ctx a:hover{color:var(--rc);background-size:100% 2px}
.ctx em{font-style:italic;color:#eaeae4}
.learn{border-left:2px solid var(--rc);padding:2px 0 2px 16px;margin:0 0 24px}
.learn p{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(15px,1.6vw,20px);
  line-height:1.34;color:var(--ink)}
.src{display:inline-flex;align-items:center;gap:9px;font-size:10px;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:var(--muted);text-decoration:none;
  transition:color .3s ease,gap .3s ease}
.src:hover{color:var(--rc);gap:14px}

@media (max-width:1080px){
  .entry{grid-template-columns:1fr;gap:30px;align-items:start}
  .media{aspect-ratio:4/3;max-height:none}
  .media--3{grid-template-rows:1.5fr 1fr}
  .txt{max-width:none}
  body{font-size:15.5px}
  .ctx{font-size:15.5px}
}
@media (max-width:680px){
  .som__grid{grid-template-columns:1fr}
  .som__r{display:none}
  .media{aspect-ratio:3/4;gap:6px}
  .hero{padding-bottom:64px}
  .entry{padding-top:88px;padding-bottom:56px}
  main{scroll-snap-type:none}
}
"""

INDEX_CSS = """
.top{padding:clamp(112px,18vh,210px) var(--pad) clamp(38px,6vh,64px)}
.top h1{font-family:var(--serif);font-weight:900;text-transform:uppercase;letter-spacing:-.025em;
  line-height:.86;font-size:clamp(50px,13.5vw,190px);margin:16px 0 0}
.top__sub{display:flex;flex-wrap:wrap;gap:10px 26px;margin-top:24px;align-items:baseline}
.top__sub p{margin:0;max-width:46ch;color:var(--muted);font-size:14px}
.wrap{padding:0 var(--pad) clamp(64px,12vh,140px)}
.blocks{display:grid;gap:14px;grid-template-columns:repeat(3,minmax(0,1fr))}
.block{position:relative;display:block;text-decoration:none;overflow:hidden;
  border:1px solid var(--line);background:var(--bg-2);
  transition:border-color .5s ease,transform .5s cubic-bezier(.22,.7,.24,1)}
.block:hover{border-color:var(--accent);transform:translateY(-3px)}
.block--lead{grid-column:1 / -1}
.slides{position:relative;width:100%;aspect-ratio:16/10;overflow:hidden;background:#0e0e10}
.block--lead .slides{aspect-ratio:21/8}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:0;transition:opacity 1.1s ease;filter:saturate(.96)}
.slides img.on{opacity:1}
.slides::after{content:"";position:absolute;inset:0;
  background:linear-gradient(to top,rgba(10,10,11,.94),rgba(10,10,11,.06) 62%)}
.block__body{position:relative;padding:clamp(18px,2.2vw,32px)}
.block__no{font-family:var(--serif);font-size:10px;font-weight:600;letter-spacing:.28em;
  color:var(--accent)}
.block__t{font-family:var(--serif);font-weight:800;text-transform:uppercase;letter-spacing:-.01em;
  line-height:1.02;font-size:clamp(19px,2.1vw,30px);margin:12px 0 12px}
.block--lead .block__t{font-size:clamp(28px,4.6vw,64px)}
.block__d{margin:0;font-size:13.5px;line-height:1.58;color:#c3c3bc;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.block--lead .block__d{font-size:15px;-webkit-line-clamp:4;max-width:70ch}
.block__hl{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:7px}
.block__hl li{font-size:12px;color:var(--muted);padding-left:16px;position:relative}
.block__hl li::before{content:"";position:absolute;left:0;top:8px;width:7px;height:1px;
  background:var(--accent)}
.block__f{display:flex;justify-content:space-between;align-items:center;gap:14px;
  margin-top:20px;padding-top:14px;border-top:1px solid var(--line)}
.block__date{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.block__go{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
.block--absent{opacity:.45;cursor:default}
.block--absent:hover{border-color:var(--line);transform:none}
.block--absent .block__go{color:var(--muted)}
@media (max-width:1020px){.blocks{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:680px){
  .blocks{grid-template-columns:1fr}
  .block--lead .slides{aspect-ratio:16/10}
  .slides img{opacity:1}
  .slides img:not(:first-child){display:none}
}
"""

REVEAL_JS = """
(function(){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); io.unobserve(e.target);} });
  },{rootMargin:'0px 0px -12% 0px',threshold:.06});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  var bar=document.querySelector('.progress');
  if(bar){
    var tick=function(){
      var h=document.documentElement.scrollHeight-window.innerHeight;
      bar.style.width=(h>0?(window.scrollY/h)*100:0)+'%';
    };
    window.addEventListener('scroll',tick,{passive:true});
    window.addEventListener('resize',tick); tick();
  }
})();
"""

SLIDES_JS = """
(function(){
  var mq=window.matchMedia('(max-width:680px)');
  document.querySelectorAll('.slides').forEach(function(box){
    var imgs=box.querySelectorAll('img'); if(imgs.length<2) return;
    var i=0,t=null;
    var step=function(){ imgs[i].classList.remove('on'); i=(i+1)%imgs.length; imgs[i].classList.add('on'); };
    var start=function(){ if(mq.matches||t) return; t=setInterval(step,2600); };
    var stop=function(){ if(!t) return; clearInterval(t); t=null;
      imgs.forEach(function(im,k){ im.classList.toggle('on',k===0); }); i=0; };
    var card=box.closest('.block')||box;
    card.addEventListener('mouseenter',start);
    card.addEventListener('mouseleave',stop);
    card.addEventListener('touchstart',function(){ t?stop():start(); },{passive:true});
  });
})();
"""

# --------------------------------------------------------------------------
# Rendu
# --------------------------------------------------------------------------


def esc(s):
    return html.escape(s or "", quote=True)


def couper(txt, n):
    """Tronque sans couper un mot en deux."""
    txt = (txt or "").strip()
    if len(txt) <= n:
        return txt
    bout = txt[:n]
    if " " in bout:
        bout = bout[:bout.rindex(" ")]
    return bout.rstrip(" ,;:") + "..."


def nom_page(iso):
    return "veille-%s.html" % iso


def bloc_media(images):
    if not images:
        return ""
    n = min(len(images), 3)
    shots = "".join(
        '<div class="shot"><img src="%s" alt="" loading="lazy" referrerpolicy="no-referrer"></div>'
        % esc(u) for u in images[:3]
    )
    return '<div class="media media--%d reveal">%s</div>' % (n, shots)


def bloc_entree(e, idx, images):
    rid = e["rubrique"]
    rc = ACCENT[rid]
    pepite = '<span class="pepite">Pépite</span>' if e["type"] == "pepite" else ""
    src = ""
    if e["source_url"]:
        src = ('<a class="src" href="%s" target="_blank" rel="noopener">%s <span>&#8599;</span></a>'
               % (esc(e["source_url"]), esc(e["source_nom"] or "Lire la source")))
    learn = ""
    if e["learning"]:
        learn = '<div class="learn reveal"><p>%s</p></div>' % esc(e["learning"])
    return """
<section class="entry" id="%(rid)s" style="--rc:%(rc)s">
  %(media)s
  <div class="txt">
    <div class="tag reveal"><span class="dot"></span><span class="tag__r">%(label)s</span>%(pep)s<span class="tag__n">%(num)s</span></div>
    <h2 class="reveal">%(titre)s</h2>
    <div class="ctx reveal">%(ctx)s</div>
    %(learn)s
    <div class="reveal">%(src)s</div>
  </div>
</section>""" % {
        "rid": esc(rid), "rc": rc, "media": bloc_media(images),
        "label": esc(LABEL[rid]), "pep": pepite, "num": "%02d" % idx,
        "titre": esc(e["titre"]), "ctx": e["contexte_html"],
        "learn": learn, "src": src,
    }


def page_edition(ed, mode, cache):
    meta = ed["meta"]
    iso = ed["date"]
    titre_en = meta.get("title_en") or "VEILLE %s" % date_courte(iso)
    deck = meta.get("deck_en") or ed["intro"] or ""
    hero = meta.get("hero_image") or ""
    if not hero:
        for e in ed["entrees"]:
            if e["images"]:
                hero = e["images"][0]
                break
    hero_src = resoudre_images([hero], mode, cache)[0] if hero else ""

    topics = meta.get("topics_fr") or []
    lignes = []
    for i, e in enumerate(ed["entrees"], start=1):
        t = topics[i - 1] if i - 1 < len(topics) else e["titre"]
        lignes.append(
            '<a class="som__row reveal" href="#%s"><span class="som__n">%02d</span>'
            '<span class="som__t">%s</span><span class="som__r">%s</span></a>'
            % (esc(e["rubrique"]), i, esc(t), esc(LABEL[e["rubrique"]]))
        )

    sections = []
    for i, e in enumerate(ed["entrees"], start=1):
        sections.append(bloc_entree(e, i, resoudre_images(e["images"], mode, cache)))

    hero_img = ('<div class="hero__img"><img src="%s" alt="" referrerpolicy="no-referrer"></div>'
                % esc(hero_src)) if hero_src else ""

    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Veille créative n°%(no)02d · %(court)s</title>
<meta name="description" content="%(desc)s">
%(fonts)s
<style>%(css)s%(css2)s</style>
</head>
<body>
<div class="progress"></div>
<div class="grain"></div>
<header class="bar">
  <a class="bar__id" href="index.html">Veille créative<span class="hide-s"> · Karl Petzold</span></a>
  <a class="btn" href="index.html">Toutes les éditions</a>
</header>
<main>
  <section class="hero">
    %(hero)s
    <div class="hero__veil"></div>
    <div class="hero__in">
      <p class="hero__no">Édition n°%(no)02d</p>
      <h1>%(titre_en)s</h1>
      <div class="hero__meta"><span class="kicker">%(longue)s</span><span class="kicker">Treize entrées</span></div>
      <p class="hero__deck">%(deck)s</p>
    </div>
    <span class="hero__scroll">Défiler</span>
  </section>
  <section class="sommaire">
    <div class="sommaire__in">
      <span class="kicker">Au sommaire</span>
      <p class="intro">%(intro)s</p>
      <div class="som__grid">%(lignes)s</div>
    </div>
  </section>
  %(sections)s
</main>
<footer>
  <span class="kicker">Veille créative · édition n°%(no)02d · %(longue)s</span>
  <a class="btn" href="index.html">Toutes les éditions</a>
</footer>
<script>%(js)s</script>
</body>
</html>""" % {
        "no": ed["numero"], "court": date_courte(iso), "longue": date_longue(iso),
        "desc": esc(couper(re.sub(r"<[^>]+>", "", deck), 180)),
        "fonts": FONTS,
        "css": BASE_CSS % {"accent": ACCENT_GLOBAL, "grain": GRAIN},
        "css2": EDITION_CSS,
        "hero": hero_img, "titre_en": esc(titre_en), "deck": esc(deck),
        "intro": esc(ed["intro"]), "lignes": "".join(lignes),
        "sections": "".join(sections), "js": REVEAL_JS,
    }


def bloc_index(ed, lead, mode, cache, dispo=True):
    meta = ed["meta"]
    titre_en = meta.get("title_en") or "Veille %s" % date_courte(ed["date"])
    deck = meta.get("deck_en") or ed["intro"] or ""
    vus, slides = set(), []
    for e in ed["entrees"]:
        for u in e["images"]:
            if u not in vus:
                vus.add(u)
                slides.append(u)
            if len(slides) >= 5:
                break
        if len(slides) >= 5:
            break
    if not slides and meta.get("hero_image"):
        slides = [meta["hero_image"]]
    slides = resoudre_images(slides, mode, cache)
    imgs = "".join('<img class="%s" src="%s" alt="" loading="lazy" referrerpolicy="no-referrer">'
                   % ("on" if i == 0 else "", esc(u)) for i, u in enumerate(slides))
    hl = ""
    if lead and meta.get("highlights"):
        hl = '<ul class="block__hl">%s</ul>' % "".join(
            "<li>%s</li>" % esc(h) for h in meta["highlights"][:3])
    if not dispo:
        return """
<div class="block block--absent reveal %(lead)s">
  <div class="slides">%(imgs)s</div>
  <div class="block__body">
    <span class="block__no">Édition n°%(no)02d</span>
    <h2 class="block__t">%(titre)s</h2>
    <p class="block__d">%(deck)s</p>
    %(hl)s
    <div class="block__f"><span class="block__date">%(date)s</span><span class="block__go">Page non publiée</span></div>
  </div>
</div>""" % {
            "lead": "block--lead" if lead else "", "imgs": imgs, "no": ed["numero"],
            "titre": esc(titre_en), "deck": esc(deck), "hl": hl,
            "date": date_longue(ed["date"]),
        }
    return """
<a class="block reveal %(lead)s" href="%(href)s">
  <div class="slides">%(imgs)s</div>
  <div class="block__body">
    <span class="block__no">Édition n°%(no)02d</span>
    <h2 class="block__t">%(titre)s</h2>
    <p class="block__d">%(deck)s</p>
    %(hl)s
    <div class="block__f"><span class="block__date">%(date)s</span><span class="block__go">Lire &#8599;</span></div>
  </div>
</a>""" % {
        "lead": "block--lead" if lead else "", "href": nom_page(ed["date"]),
        "imgs": imgs, "no": ed["numero"], "titre": esc(titre_en),
        "deck": esc(deck), "hl": hl, "date": date_longue(ed["date"]),
    }


def page_index(editions, mode, cache, dossier="."):
    ordre = sorted(editions, key=lambda e: e["date"], reverse=True)

    def dispo(ed):
        return os.path.exists(os.path.join(dossier, nom_page(ed["date"])))

    blocs = [bloc_index(ordre[0], True, mode, cache, dispo(ordre[0]))] if ordre else []
    blocs += [bloc_index(ed, False, mode, cache, dispo(ed)) for ed in ordre[1:]]
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Veille créative · Karl Petzold</title>
<meta name="description" content="Revue hebdomadaire : direction artistique, mode, luxe, craft, architecture, scénographie, photographie, film, illustration, gaming, interface, IA, philosophie.">
%(fonts)s
<style>%(css)s%(css2)s</style>
</head>
<body>
<div class="grain"></div>
<header class="bar"><a class="bar__id" href="index.html">Veille créative<span class="hide-s"> · Karl Petzold</span></a>
<span class="kicker">%(n)d éditions</span></header>
<section class="top">
  <span class="kicker">Revue hebdomadaire</span>
  <h1>Veille<br>créative</h1>
  <div class="top__sub">
    <p>Treize rubriques, une entrée par rubrique. Ce qui apprend à faire, à voir ou à anticiper.</p>
    <span class="kicker">Dernière édition : %(dern)s</span>
  </div>
</section>
<div class="wrap"><div class="blocks">%(blocs)s</div></div>
<footer><span class="kicker">Karl Petzold · Pavillon Noir</span><span class="kicker">%(n)d éditions archivées</span></footer>
<script>%(js1)s%(js2)s</script>
</body>
</html>""" % {
        "fonts": FONTS,
        "css": BASE_CSS % {"accent": ACCENT_GLOBAL, "grain": GRAIN},
        "css2": INDEX_CSS,
        "n": len(editions),
        "dern": date_longue(ordre[0]["date"]) if ordre else "",
        "blocs": "".join(blocs), "js1": REVEAL_JS, "js2": SLIDES_JS,
    }


# --------------------------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        sys.stderr.write("Usage : python3 build.py data-AAAA-MM-JJ.json ./ [--images=inline]\n")
        return 1
    data_path = args[0]
    dossier = args[1] if len(args) > 1 else "."
    mode = "inline" if any(o.startswith("--images=inline") for o in opts) else "url"

    if not os.path.exists(data_path):
        sys.stderr.write("Fichier introuvable : %s\n" % data_path)
        return 1

    editions = charger_editions(dossier)
    if not editions:
        sys.stderr.write("Aucun data*.json exploitable dans %s\n" % dossier)
        return 1

    cible_iso = normaliser(data_path)["date"]
    cible = next((e for e in editions if e["date"] == cible_iso), None)
    if cible is None:
        sys.stderr.write("L'édition %s n'a pas été retrouvée dans le dossier.\n" % cible_iso)
        return 1

    cache = {}
    sortie = os.path.join(dossier, nom_page(cible_iso))
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(page_edition(cible, "url", cache))
    print("Page de l'édition n°%02d : %s" % (cible["numero"], sortie))

    idx = os.path.join(dossier, "index.html")
    with open(idx, "w", encoding="utf-8") as f:
        f.write(page_index(editions, "url", cache, dossier))
    print("Archive régénérée : %s (%d éditions)" % (idx, len(editions)))

    if mode == "inline":
        art = os.path.join(dossier, "artefact-%s.html" % cible_iso)
        with open(art, "w", encoding="utf-8") as f:
            f.write(page_edition(cible, "inline", cache))
        print("Version artefact, images embarquées : %s" % art)

    return 0


if __name__ == "__main__":
    sys.exit(main())
