# DA-SPEC — Veille créative hebdomadaire

**Direction artistique prescriptive. Version 1.0 — 2026-08-31.**
Document contraignant pour le développement UI/UX. Tout ce qui est écrit ici est à appliquer à la lettre.
Les valeurs sont exactes : ne pas « arrondir », ne pas substituer une couleur, une durée ou une courbe.

---

## 0. INTENTION

Un magazine, pas un blog. Le contenu est éditorial, français, dense, cultivé — craft japonais, osier tressé, donjons de bois déplacés à la corde, caméras grand capteur, manuscrits médiévaux. La DA doit avoir **la tenue d'un papier haut de gamme et la brutalité d'un lookbook hypebeast**.

Trois règles qui priment sur tout le reste :

1. **Le noir et blanc porte l'image, l'acide porte la structure.** Aucune photo n'est colorée au repos. La seule couleur de la page est l'accent, et il ne touche jamais une photo.
2. **Le vide est un matériau.** Marges généreuses, respirations larges, jamais de remplissage. Un bloc à moitié vide est un bloc réussi.
3. **Une seule chose crie par écran.** Un display, ou un numéro, ou une image. Jamais deux.

Corollaire technique : **les couleurs `accent` par rubrique présentes dans les anciens JSON (`#c9a24a`, `#9b7ec9`, etc.) sont abandonnées.** `build.py` doit les ignorer. Le système est strictement monochrome + un accent unique.

---

## 1. PALETTE

### 1.1 Choix de l'accent

**`--accent: #D9FF3D` — un citron-chartreuse acide, légèrement tiré vers le vert.**

Pourquoi celui-ci : c'est la seule famille chromatique qui soit à la fois *tech/industrielle* (marquage de sécurité, sérigraphie technique, workwear) et *couture* (l'acide chartreuse est la teinte signature du luxe post-2020 quand il veut trancher) — il parle donc simultanément aux deux moitiés du contenu, le craft patrimonial et l'actualité hypebeast. Et sur des photos N&B légèrement chaudes (argent, cuivre, bois, chaume), un vert-jaune froid est la complémentaire exacte : il ne se fond jamais dans l'image, il la découpe.

### 1.2 Tokens

Bloc à copier tel quel dans `:root`.

```css
:root{
  /* ---- fonds ---- */
  --bg:            #0C0C0E;   /* encre presque noire, très légèrement froide */
  --surface:       #141417;   /* blocs accueil, cartes, panneaux */
  --surface-2:     #1C1C21;   /* survol de surface, champs, médaillons */
  --surface-accent:#24271A;   /* = accent 8% composé sur --surface (hover de bloc) */

  /* ---- texte ---- */
  --ink:           #F5F2EC;   /* primaire — blanc papier chaud, jamais #FFF */
  --ink-2:         #C3C0B8;   /* secondaire — chapôs, contexte, légendes longues */
  --muted:         #93908A;   /* tertiaire — dates, sources, compteurs, méta */

  /* ---- filets & surfaces ---- */
  --line:          rgba(245,242,236,.12);  /* filet standard (≈ #29292B sur --bg) */
  --line-strong:   rgba(245,242,236,.26);  /* filet de section, hover de filet */
  --line-accent:   #D9FF3D;                /* filet d'état actif uniquement */

  /* ---- accent ---- */
  --accent:        #D9FF3D;
  --accent-ink:    #0C0C0E;   /* SEUL texte autorisé sur un aplat d'accent */
  --accent-wash:   rgba(217,255,61,.08);
  --accent-line:   rgba(217,255,61,.35);

  /* ---- scrims photo ---- */
  --scrim-top:     rgba(12,12,14,.35);
  --scrim-bottom:  rgba(12,12,14,.88);
  --scrim-flat:    rgba(12,12,14,.72);  /* voile plein minimum sous un texte */
}
```

### 1.3 Loi de l'accent — usages AUTORISÉS

L'accent est rare. **Cible : ≤ 3 % de la surface d'un écran, ≤ 4 occurrences visibles simultanément.** Si un écran en contient plus, il est en faute.

| # | Usage autorisé | Forme |
|---|---|---|
| 1 | **Numéro d'édition** — le chiffre géant du hero (`03`) | texte plein `--accent` |
| 2 | **Kicker de rubrique** — le mot de rubrique en full caps au-dessus d'un titre de news | texte plein `--accent` |
| 3 | **Filet actif** — soulignement d'un lien au hover, barre de progression remplie, filet gauche de la news courante | trait 1px ou 2px |
| 4 | **Marqueur de fin** — le carré plein de 6×6 px qui clôt un `learning` | aplat |
| 5 | **Anneau de focus clavier** | `outline: 2px solid var(--accent)` |
| 6 | **Un seul aplat par page maximum** — le bouton « Lire l'édition » du bloc en vedette | fond `--accent`, texte `--accent-ink` |
| 7 | **Wash de survol** (`--accent-wash`) sur un bloc accueil | fond, invisible ou presque |

### 1.4 Loi de l'accent — usages INTERDITS

- ❌ **Jamais sur une photo** : pas de duotone acide, pas de teinte d'image, pas d'overlay coloré. Les images restent N&B ou couleur, jamais accentuées.
- ❌ **Jamais un paragraphe** ni une phrase complète en accent. Maximum : 6 mots.
- ❌ **Jamais `--ink` sur `--accent`** (ratio mesuré 1,03:1 — illisible). Sur un aplat accent, le texte est `--accent-ink`, point.
- ❌ **Jamais deux aplats d'accent visibles dans le même viewport.** Deux exceptions nommées, et aucune autre : le badge `PÉPITE` d'une news (§5.5) et le curseur de survol (§6.6). Quand le curseur `VOIR` est actif sur l'accueil, il est **le seul** aplat visible — il n'apparaît pas au survol du bloc vedette, dont le bouton `LIRE L'ÉDITION` occupe déjà ce rôle.
- ❌ **Jamais en couleur de bordure permanente** d'un bloc (l'accent marque l'état, pas la structure).
- ❌ **Jamais dégradé, jamais glow, jamais `box-shadow` coloré.** L'accent est plat, sérigraphique, mat.
- ❌ **Aucune seconde couleur** n'est introduite. Pas de rouge d'erreur, pas de vert de succès : les états système reprennent `--ink` / `--muted` / `--accent`.

---

## 2. TYPOGRAPHIE

### 2.1 Chargement

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@700;800;900&family=Outfit:wght@700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

`display=swap` obligatoire. Les trois familles seulement, aucune autre graisse que celles listées (poids de page).

```css
:root{
  --font-display: "Unbounded", "Outfit", ui-sans-serif, system-ui, sans-serif;
  --font-ui:      "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
}
```

### 2.2 Rôles

| Rôle | Famille | Graisse | Casse | Letter-spacing |
|---|---|---|---|---|
| **Display hero** (titre d'édition) | Unbounded (fb. Outfit) | **900** | Titre, tel quel | `-0.035em` |
| **Titre de bloc accueil** | Unbounded (fb. Outfit) | **800** | Titre | `-0.03em` |
| **Titre de news** | Unbounded (fb. Outfit) | **800** | Phrase (français, casse naturelle) | `-0.025em` |
| **Chiffre d'édition géant** | Unbounded | **900** | — | `-0.05em` |
| **Kicker / label / rubrique** | Inter | **500** | `text-transform: uppercase` | **`0.18em`** |
| **Date / source / compteur** | Inter | **500** | `uppercase` | **`0.14em`** |
| **Micro-label** (≤ 11px : compteur, index) | Inter | **600** | `uppercase` | **`0.22em`** |
| **Chapô / lead** | Inter | **400** | naturelle | `-0.005em` |
| **Corps** | Inter | **400** | naturelle | `0` |
| **Learning** (l'enseignement en fin de news) | Inter | **500**, `font-style: italic` non — **roman** | naturelle | `-0.01em` |
| **Caption image** | Inter | **500** | naturelle | `0.01em` |

Règles absolues :
- **Unbounded n'est JAMAIS en full caps.** Trop de matière, illisible. Les caps sont le territoire exclusif d'Inter.
- **Tout ce qui est en full caps porte du letterspacing.** Aucune exception. Full caps sans letterspacing = bug.
- Le letterspacing des caps ne descend jamais sous `0.14em` ni ne monte au-dessus de `0.22em`.
- Titres Unbounded : `text-wrap: balance;` et `hyphens: none;`.
- Corps : `text-wrap: pretty;`, `max-width: 68ch` en une colonne, `hyphens: auto; lang="fr"`.

### 2.3 Échelle — tokens `clamp()`

Base desktop cible 1440 px. Toutes les bornes basses correspondent au mobile 375 px.

```css
:root{
  /* --- display --- */
  --t-hero:      clamp(3.00rem, 1.10rem + 8.10vw, 8.50rem);  /* 48 → 136px */
  --t-numeral:   clamp(4.50rem, 1.20rem + 14.0vw, 15.00rem); /* 72 → 240px */
  --t-block-xl:  clamp(2.25rem, 1.05rem + 5.10vw, 4.25rem);  /* 36 → 68px  — bloc vedette */
  --t-block:     clamp(1.50rem, 0.95rem + 2.35vw, 2.50rem);  /* 24 → 40px  — blocs standard */
  --t-news:      clamp(1.95rem, 0.90rem + 4.45vw, 4.00rem);  /* 31 → 64px  — titre de news */
  --t-section:   clamp(1.25rem, 0.90rem + 1.50vw, 2.00rem);  /* 20 → 32px  — titres de section */

  /* --- Inter --- */
  --t-lead:      clamp(1.0625rem, 0.94rem + 0.55vw, 1.4375rem); /* 17 → 23px */
  --t-body:      clamp(0.9375rem, 0.88rem + 0.26vw, 1.125rem);  /* 15 → 18px */
  --t-small:     clamp(0.8125rem, 0.79rem + 0.13vw, 0.9375rem); /* 13 → 15px */
  --t-kicker:    clamp(0.6875rem, 0.66rem + 0.13vw, 0.8125rem); /* 11 → 13px */
  --t-micro:     clamp(0.625rem,  0.61rem + 0.07vw, 0.6875rem); /* 10 → 11px */

  /* --- interlignages --- */
  --lh-numeral: 0.78;
  --lh-hero:    0.90;
  --lh-display: 0.98;   /* titres de blocs & de news */
  --lh-section: 1.10;
  --lh-lead:    1.42;
  --lh-body:    1.62;
  --lh-caps:    1.25;   /* kickers, labels, dates */
  --lh-small:   1.50;
}
```

Application :

```css
.hero-title { font: 900 var(--t-hero)/var(--lh-hero) var(--font-display); letter-spacing:-.035em; }
.edition-num{ font: 900 var(--t-numeral)/var(--lh-numeral) var(--font-display); letter-spacing:-.05em; color:var(--accent); }
.block-title{ font: 800 var(--t-block)/var(--lh-display) var(--font-display); letter-spacing:-.03em; }
.news-title { font: 800 var(--t-news)/var(--lh-display) var(--font-display); letter-spacing:-.025em; }
.kicker     { font: 500 var(--t-kicker)/var(--lh-caps) var(--font-ui); letter-spacing:.18em; text-transform:uppercase; color:var(--accent); }
.meta       { font: 500 var(--t-kicker)/var(--lh-caps) var(--font-ui); letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.micro      { font: 600 var(--t-micro)/var(--lh-caps)  var(--font-ui); letter-spacing:.22em; text-transform:uppercase; color:var(--muted); }
.lead       { font: 400 var(--t-lead)/var(--lh-lead)   var(--font-ui); color:var(--ink-2); letter-spacing:-.005em; }
.body       { font: 400 var(--t-body)/var(--lh-body)   var(--font-ui); color:var(--ink-2); }
.caption    { font: 500 var(--t-small)/var(--lh-small) var(--font-ui); color:var(--muted); }
.learning   { font: 500 var(--t-lead)/1.48 var(--font-ui); color:var(--ink); letter-spacing:-.01em; }
```

Le `contexte_html` du JSON contient des `<a>` : dans le corps, un lien est `color: var(--ink)`, `text-decoration: underline`, `text-underline-offset: .22em`, `text-decoration-thickness: 1px`, `text-decoration-color: var(--line-strong)` → au hover `text-decoration-color: var(--accent)`.

---

## 3. MATIÈRE & TEXTURE

### 3.1 Grain — l'élément le plus important de la DA

Deux couches distinctes, jamais confondues.

**Couche A — grain global de page (fin, permanent).** Appliqué une fois sur `body::after`, `position: fixed`, plein écran, `pointer-events:none`, `z-index: 9999`.

```css
body::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9999;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.86' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:200px 200px;
  opacity:.055;
  mix-blend-mode:overlay;
}
```

Valeurs verrouillées : `baseFrequency 0.86`, `numOctaves 4`, `stitchTiles stitch` (sans quoi les tuiles se voient), `saturate 0` (le grain n'est jamais coloré), tuile **200 px**, `opacity .055`, `mix-blend-mode: overlay`.

**Couche B — grain argentique du hero (gros, lourd).** Sur `.hero::after` uniquement, par-dessus la photo, sous le texte.

```css
.hero::after{
  content:""; position:absolute; inset:0; pointer-events:none; z-index:2;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='340' height='340'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.42' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3CfeComponentTransfer%3E%3CfeFuncA type='linear' slope='1.35' intercept='-0.18'/%3E%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='340' height='340' filter='url(%23g)'/%3E%3C/svg%3E");
  background-size:340px 340px;
  opacity:.16;
  mix-blend-mode:soft-light;
}
```

Le `feComponentTransfer` (slope 1.35 / intercept −0.18) écrase les mi-tons du bruit et ne garde que les pointes : c'est ce qui donne un grain d'émulsion et non un bruit de compression. Ne pas le retirer.

**Interdits :** aucun grain animé (coûteux, et ça fait démo WebGL, pas magazine). Aucun grain en `<canvas>`. Aucun grain sur les images d'articles (couche A suffit, elle passe par-dessus tout).

### 3.2 Traitement du hero (photo N&B atmosphérique)

Les images hero arrivent en couleur du CDN. Elles sont **désaturées en CSS**, pas en amont, pour rester échangeables.

```css
.hero-img{
  width:100%; height:100%; object-fit:cover; object-position:center 42%;
  filter: grayscale(1) contrast(1.08) brightness(.80) saturate(0);
  transform: scale(1.04);           /* réserve pour le parallax, cf. §4.6 */
  will-change: transform;
}
```

`brightness(.80)` est un plancher : il garantit qu'aucune photo importée ne fera exploser le contraste du texte. Ne pas le supprimer même si une photo paraît sombre.

**Duotone : autorisé, chaud, discret.** Pas d'accent. Un voile bi-ton qui pousse les ombres vers `--bg` et réchauffe les hautes lumières vers `--ink` — c'est ce qui donne la sensation « tirage argentique » plutôt que « N&B numérique ».

```css
.hero-duotone{                       /* calque dédié, au-dessus de .hero-img, sous les scrims */
  position:absolute; inset:0; z-index:1; pointer-events:none;
  background:linear-gradient(180deg, #F5F2EC 0%, #0C0C0E 100%);
  mix-blend-mode:soft-light; opacity:.22;
}
```

**Scrims de lisibilité — obligatoires, non négociables.** Trois couches empilées sur `.hero`, dans cet ordre (du fond vers le texte) :

```css
.hero-scrim{
  position:absolute; inset:0; z-index:3; pointer-events:none;
  background:
    /* 1. voile bas : porte le titre + le paragraphe */
    linear-gradient(to top,
      rgba(12,12,14,.94) 0%,
      rgba(12,12,14,.86) 22%,
      rgba(12,12,14,.54) 48%,
      rgba(12,12,14,.18) 72%,
      rgba(12,12,14,0)   100%),
    /* 2. voile haut : porte le header + le numéro d'édition */
    linear-gradient(to bottom, rgba(12,12,14,.62) 0%, rgba(12,12,14,0) 34%),
    /* 3. plancher plat : sécurité contre une photo très claire */
    linear-gradient(rgba(12,12,14,.22), rgba(12,12,14,.22));
}
```

**Règle de sécurité mesurée (cf. §8) :** sous le bloc de texte du hero, l'opacité cumulée du scrim ne descend **jamais sous 0,78**. Au-dessus de 0,72, `--ink`, `--ink-2` et `--accent` passent tous ; **`--muted` est INTERDIT sur photo** (mesuré 2,38:1 à 62 % de scrim sur une haute lumière). La date et le numéro en méta sur le hero utilisent `--ink-2`, pas `--muted`.

Transition bas de hero → contenu : les 120 derniers pixels du hero se fondent dans `--bg` via le stop à `.94`, sans filet de séparation. Le hero ne se termine pas par une ligne, il s'éteint.

### 3.3 Traitement des images d'articles

**Au repos : N&B. Au hover : couleur.** C'est la signature interactive du site — la page est un contact sheet, le survol « développe » l'image.

```css
.news-img, .block-img{
  filter: grayscale(1) contrast(1.05) brightness(.92);
  transition: filter 520ms var(--ease-out), transform 900ms var(--ease-out);
  transform: scale(1.0);
}
.news-fig:hover .news-img,
.block:hover .block-img{
  filter: grayscale(0) contrast(1.02) brightness(1);
  transform: scale(1.035);
}
```

- La désaturation part **avant** le retour de la couleur en sortie de hover : sortie = `filter 340ms`. (Entrée douce, sortie nette.)
- **Sur touch (`@media (hover:none)`) : les images d'articles sont en couleur en permanence** (`filter: contrast(1.03)`), il n'y a pas d'état de repos N&B qu'on ne peut pas révéler.
- Les images du **slideshow des blocs d'accueil restent N&B en toutes circonstances** — c'est là que le N&B fait la cohérence de la home. Le passage à la couleur est réservé aux pages édition.

**Tranche / cadre des images :** aucune bordure, aucun `border-radius` (le radius est banni du système, cf. §6.2), aucune ombre portée. Une image est posée sur `--surface` et se termine par un **filet 1px `--line` en bas uniquement** quand elle est suivie d'une légende ; sinon rien.

Toutes les images d'articles : `loading="lazy"`, `decoding="async"`, `referrerpolicy="no-referrer"`, ratio réservé en CSS (`aspect-ratio`) pour zéro CLS. Le hero seul est `loading="eager"` + `fetchpriority="high"`.

---

## 4. MOTION

### 4.1 Tokens

```css
:root{
  --d-instant: 120ms;   /* changement de couleur, opacité d'un micro-élément */
  --d-fast:    220ms;   /* hover de lien, de label, de filet */
  --d-base:    380ms;   /* hover de bloc, apparition d'un panneau */
  --d-slow:    620ms;   /* reveal au scroll, image */
  --d-scene:   900ms;   /* transition de section plein écran */

  --ease-out:   cubic-bezier(.16, 1, .30, 1);    /* sortie expo — le défaut */
  --ease-inout: cubic-bezier(.65, 0, .35, 1);    /* aller-retour symétrique */
  --ease-edito: cubic-bezier(.22, 1, .36, 1);    /* reveals, scroll magnétique */
  --ease-snap:  cubic-bezier(.83, 0, .17, 1);    /* cut, bascule d'état */
}
```

`--ease-out` est le défaut de tout ce qui n'est pas spécifié. **Aucune animation n'utilise `linear`, `ease`, `ease-in-out` par défaut.** Aucun rebond, aucun `back`, aucun `elastic` : le luxe ne rebondit pas.

### 4.2 Hover — blocs d'accueil

Au survol d'un bloc, **quatre choses bougent ensemble**, et rien d'autre :

```css
.block{
  background:var(--surface);
  border:1px solid var(--line);
  transition:
    background var(--d-base) var(--ease-out),
    border-color var(--d-base) var(--ease-out),
    transform var(--d-base) var(--ease-out);
}
.block:hover{
  background:var(--surface-accent);      /* #24271A */
  border-color:var(--line-strong);
  transform:translateY(-3px);             /* JAMAIS plus de 4px */
}
.block:hover .block-title{ color:var(--ink); }       /* depuis --ink-2 : cf. §5.2, le titre est --ink-2 au repos */
.block:hover .block-cta  { color:var(--accent); }    /* le seul point d'accent qui apparaît */
```

**Cas du bloc vedette** (photo plein cadre : le changement de `background` ne se verrait pas). À la place, au hover : le scrim s'éclaircit (`opacity` du calque scrim `1 → .82`, `--d-base`), le slideshow démarre, la bordure passe `--line-strong`, `translateY(-3px)` identique. Pas de `--surface-accent`.

Interdits sur hover de bloc : `scale` du bloc entier, ombre portée, changement de radius, rotation, `filter: brightness` sur le bloc.

### 4.3 Hover — liens & labels

Soulignement qui se dessine de gauche à droite, jamais un `text-decoration` qui apparaît d'un coup :

```css
.link{ position:relative; color:var(--ink); }
.link::after{
  content:""; position:absolute; left:0; right:0; bottom:-.18em; height:1px;
  background:var(--accent); transform:scaleX(0); transform-origin:left;
  transition:transform var(--d-fast) var(--ease-out);
}
.link:hover::after{ transform:scaleX(1); }
.link:hover{ color:var(--accent); }        /* uniquement pour les liens courts / CTA */
```

Pour un lien **dans un paragraphe**, on ne change pas la couleur du texte (ça pique le paragraphe) : seul `text-decoration-color` passe à `--accent` en `var(--d-fast)`.

Labels et kickers au survol de leur bloc parent : `letter-spacing` passe de `.18em` à `.22em` en `var(--d-base) var(--ease-out)`. Micro-détail, très perceptible, très magazine. **Ne jamais animer le letter-spacing d'un texte long** (reflow).

### 4.4 Reveals au scroll

`IntersectionObserver` (`threshold: 0.15`, `rootMargin: "0px 0px -12% 0px"`), classe `.is-in` ajoutée une fois, **jamais retirée** (pas de re-animation au scroll arrière — c'est la marque des sites cheap).

```css
.reveal{
  opacity:0; transform:translateY(18px);
  transition: opacity var(--d-slow) var(--ease-edito), transform var(--d-slow) var(--ease-edito);
}
.reveal.is-in{ opacity:1; transform:none; }
```

- Déplacement **18 px maximum**. Jamais 40, jamais 60.
- Aucun `scale` au reveal, aucun `blur` au reveal, aucune rotation.
- **Stagger** dans un groupe : `transition-delay: calc(var(--i) * 70ms)`, plafonné à **5 items** (`--i` max 4). Au-delà, tout part ensemble.
- Les titres Unbounded ne se révèlent **pas** lettre par lettre ni mot par mot. Bloc entier.
- Un reveal ne doit jamais empêcher la lecture : si l'élément est déjà dans le viewport au chargement, il est `.is-in` immédiatement (initialiser l'observer après un `requestAnimationFrame`, pas de flash).

### 4.5 Slideshow des blocs d'accueil (5 images)

**Cut sec éditorial, pas de crossfade.** Le crossfade fait « diaporama de mariage ». Le cut fait « défilement de planche-contact ». C'est un choix ferme.

- Cadence : **420 ms par image** (≈ 2,4 img/s). Rythme rapide, nerveux, hypebeast.
- Technique : les 5 `<img>` sont empilées en absolu, `opacity: 0`, l'active `opacity: 1`, avec `transition: opacity 90ms linear` — 90 ms est le seuil qui supprime le scintillement de repaint sans créer de fondu perceptible. **C'est la seule occurrence de `linear` autorisée du système.**
- Démarrage : au `pointerenter`, **après un délai de 120 ms** (évite le déclenchement au passage de souris traversant).
- Arrêt : au `pointerleave`, retour à l'image 0 **immédiatement** (`opacity` cut, 0 ms). Pas de retour progressif.
- La première image est celle affichée au repos ; le cycle démarre donc à l'image 1, boucle 1→2→3→4→0→1…
- Les images 1-4 sont chargées en `loading="lazy"` mais **préchargées au premier `pointerenter`** (passer `loading="eager"` en JS) pour qu'aucun cut ne tombe sur une image vide.
- Un seul slideshow actif à la fois sur la page : le `pointerenter` d'un bloc arrête tous les autres.
- **N'existe pas au touch** → cf. §7.4.

### 4.6 Hero

- **Parallax** : la photo se déplace de `translate3d(0, calc(var(--sy) * .18), 0)` où `--sy` est le scroll dans le hero — soit **18 % de la vitesse de scroll**, plafonné à 120 px. Calculé dans un `requestAnimationFrame` throttlé, pas dans un `scroll` listener nu.
- **Fade sortant** : le bloc de texte du hero passe de `opacity 1` à `0.15` et `translateY(-24px)` entre 0 % et 60 % de la hauteur de hero scrollée. Courbe `--ease-edito`, piloté par la position, pas par une transition.
- **Entrée au chargement** : la photo `scale(1.08) → scale(1.04)` en `1400ms var(--ease-edito)` + `opacity 0 → 1` en `900ms`. Le texte suit en stagger 70 ms (numéro, puis titre, puis date, puis paragraphe), chacun `--d-slow`.

### 4.7 Scroll magnétique des news (le morceau de bravoure)

Comportement voulu : le scroll **prend de la vitesse au départ, puis freine longuement à l'approche** de la news suivante. Pas un snap sec, pas un scroll libre.

**Base CSS (fonctionne seule, sans JS) :**

```css
.news-track{ scroll-snap-type: y mandatory; }   /* sur le conteneur scrollable */
.news-section{
  min-height:100svh;
  scroll-snap-align:start;
  scroll-snap-stop:always;    /* interdit de sauter une news d'un geste large */
}
```

**Assistance JS (obligatoire, sinon le feel n'y est pas) :**

- Intercepter `wheel` (`{passive:false}`) et `touchstart/touchmove/touchend` sur `.news-track`.
- Un geste déclenche une **transition d'une seule section** si `|deltaY| > 12` (souris) ou si le swipe dépasse `60px` ou `0.35 px/ms` de vélocité (tactile).
- Pendant l'animation : **verrou** `isAnimating = true`, tous les événements de scroll sont annulés (`preventDefault`). Déverrouillage à la fin + **cooldown de 140 ms**.
- Animation : `scrollTop` interpolé sur **780 ms** avec la courbe `--ease-edito` = `cubic-bezier(.22, 1, .36, 1)` évaluée en JS (implémenter le solveur bezier ; ne pas approximer par un `easeOutCubic`, le freinage long est précisément ce qu'on cherche). Alternative acceptée : `scrollTo({behavior:'smooth'})` **refusée** — la courbe navigateur est trop plate.
- **Distance longue** (saut clavier `Home`/`End`, ancre) : durée `780ms + 120ms par section supplémentaire`, plafond **1400 ms**.
- Clavier : `↓`/`↑`, `PageDown`/`PageUp`, `Espace` déclenchent la même transition d'une section. **Le hijack ne doit jamais bloquer `Tab`** : si le focus passe à un élément d'une autre section, on y va avec la même animation.
- Le hijack est **actif uniquement sur `.news-track`** et **uniquement à partir de 900 px de large** (cf. §7.4). Le hero et le récap scrollent normalement.
- Sécurité : si `matchMedia('(prefers-reduced-motion: reduce)')` → hijack entièrement désactivé, `scroll-snap-type: y proximity`, `scroll-behavior: auto`.
- Sécurité 2 : si l'utilisateur scrolle pendant 3 gestes contrariés en moins de 600 ms (il se bat avec la page), désactiver le hijack pour la session et laisser `scroll-snap: proximity`.

### 4.8 `prefers-reduced-motion`

Bloc à copier tel quel, en fin de feuille :

```css
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration:.01ms !important;
    animation-iteration-count:1 !important;
    transition-duration:.01ms !important;
    scroll-behavior:auto !important;
  }
  .reveal{ opacity:1 !important; transform:none !important; }
  .news-track{ scroll-snap-type: y proximity; }
  .hero-img{ transform:none !important; }
}
```

En JS, en plus : slideshow **désactivé** (image 0 fixe), parallax désactivé, scroll hijack désactivé, stagger à 0. Les changements de **couleur** restent (à `.01ms` ils sont instantanés, c'est acceptable et ça préserve l'affordance de hover).

---

## 5. COMPOSITION

### 5.1 Grille & mesures globales

```css
:root{
  --maxw:      1560px;         /* conteneur principal */
  --maxw-text: 68ch;           /* colonne de lecture */
  --pad-x:     clamp(20px, 4.2vw, 72px);
  --gutter:    clamp(14px, 1.6vw, 28px);
  --gap-block: clamp(48px, 6vw, 120px);   /* entre grandes sections */
}
.wrap{ width:100%; max-width:var(--maxw); margin-inline:auto; padding-inline:var(--pad-x); }
```

Grille **12 colonnes**, `display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--gutter);`.
Rythme vertical : multiples de **8 px**. Aucune valeur d'espacement impaire.

### 5.2 Accueil — blocs rectangulaires

Structure : un bloc **vedette** (dernière édition) + N blocs standard. Pas de liste de news, scroll minimal — la home doit tenir en **1,5 écran pour 3 éditions**.

```
┌───────────────────────────────────────────────────────────┐
│  BLOC VEDETTE — 12 col — aspect-ratio 21/9 (desktop)      │
│  slideshow plein cadre en fond, scrim, texte en bas-gauche│
└───────────────────────────────────────────────────────────┘
┌────────────────────────────┐ ┌────────────────────────────┐
│ BLOC — 6 col — ratio 4/3   │ │ BLOC — 6 col — ratio 4/3   │
└────────────────────────────┘ └────────────────────────────┘
```

**Proportions exactes :**

| | Colonnes | `aspect-ratio` | Titre | Padding interne |
|---|---|---|---|---|
| Vedette | 12 / 12 | `21 / 9` (min-height `440px`) | `--t-block-xl` | `clamp(28px, 3.4vw, 56px)` |
| Standard | 6 / 12 | `4 / 3` | `--t-block` | `clamp(22px, 2.2vw, 36px)` |

Le bloc vedette fait donc **≈ 2,3× la surface** d'un bloc standard : la hiérarchie est franche, pas timide.

**Ce qui distingue visuellement la vedette** (cumuler les 5, c'est ce qui la fait « se démarquer ») :
1. Le slideshow occupe **tout le cadre** en fond (les standards ont l'image dans la moitié haute seulement, ratio `16/9` interne).
2. Un **eyebrow** `DERNIÈRE ÉDITION` en `.micro`, couleur `--accent`, en haut à gauche, précédé d'un carré plein 6×6 px accent.
3. Le **numéro d'édition** en `--t-block-xl` Unbounded 900, en haut à droite, `color: var(--line-strong)` — un chiffre fantôme.
4. Une **description de 3 lignes** (`--t-lead`) là où les standards en ont 2 (`--t-body`).
5. Le **seul aplat d'accent de la page** : le bouton `LIRE L'ÉDITION →` (fond `--accent`, texte `--accent-ink`, `.micro`, padding `14px 22px`).

Contenu d'un bloc standard, de haut en bas : image/slideshow → filet `--line` pleine largeur → `.meta` (date FR + « 13 entrées ») → titre anglais (`--t-block`, **`--ink-2` au repos, `--ink` au hover** — cf. §4.2) → description 2 lignes (`--ink-2`, `line-clamp: 2`) → `.micro` `LIRE →` en `--muted`, passe `--accent` au hover.

Sur le bloc vedette, le titre est en `--ink` dès le repos (c'est lui qui doit crier) ; seul son `.block-cta` change au hover.

Le bloc entier est un `<a>` (cible cliquable pleine surface), pas un div avec un lien dedans.

### 5.3 Page édition — hero plein écran

`height: 100svh` (pas `100vh` — barre d'URL mobile), `min-height: 640px`, `position: relative; overflow: hidden`.

Placement, grille 12 colonnes, texte ancré en **bas à gauche**, `padding-bottom: clamp(48px, 8vh, 104px)` :

```
┌──────────────────────────────────────────────── 100svh ──┐
│ ÉDITION 03        [ header : logo + archive ]            │  ← .micro --ink-2, top-left sous le header
│                                                          │
│                                                          │
│  03                                                      │  ← --t-numeral, accent, col 1-3
│                                                          │
│  SLOW HANDS,                        VENDREDI 28 AOÛT 2026│  ← titre col 1-8 / date .meta col 10-12,
│  FAST MACHINES                      13 ENTRÉES           │    alignée sur la BASELINE de la 1re ligne du titre
│  ────────────────────────────                            │  ← filet --line-strong, 1px, col 1-6
│  Trois pépites hors actualité portent le craft…          │  ← --lead, --ink-2, col 1-6, max 3 lignes
│                                                          │
│                                    ↓ DÉFILER             │  ← .micro --muted, bas-droite
└──────────────────────────────────────────────────────────┘
```

- Le **numéro géant** (`03`) est posé directement au-dessus du titre, aligné sur la même colonne, **sans espace** (`margin-bottom: -.06em` — le chiffre et le titre doivent se toucher optiquement).
- La **date** est en haut à droite du titre, alignée sur la **première baseline** du titre, jamais centrée verticalement.
- Le paragraphe est limité à **3 lignes** et `max-width: 46ch`. S'il déborde, on coupe — le hero ne s'allonge pas.
- L'indicateur `↓ DÉFILER` disparaît (`opacity 0`, `--d-base`) dès 40 px de scroll.

### 5.4 Page édition — récap après le hero

Une seule section, courte, sur `--bg`, `padding-block: var(--gap-block)`.

- Colonne gauche (col 1-4) : `.micro` `AU SOMMAIRE` + le nombre d'entrées en Unbounded 800 `--t-section`.
- Colonne droite (col 6-12) : le paragraphe d'intro (`--lead`, max 3 lignes), puis **la liste des sujets** : une ligne par entrée, chacune = `<rubrique en .kicker --muted, largeur fixe 168px> + <résumé ultra bref, --t-body --ink-2>`, séparées par un filet `--line` 1px pleine largeur.
- Chaque ligne est un lien d'ancre vers sa news ; au hover : le fond passe `--surface`, la rubrique passe `--accent`, un `→` apparaît à droite (`translateX(-8px) → 0`, `--d-fast`).
- Hauteur de ligne : `56px` desktop / `auto` (empilé) sous 768 px.

### 5.5 Page édition — news plein écran

Chaque news = `<section class="news-section">`, `min-height: 100svh`, `display: grid` 12 colonnes, alignement `center`.

**Alternance de deux gabarits** (impair = A, pair = B) pour casser la monotonie sur 13 sections :

**Gabarit A — texte à gauche (col 1-5), images à droite (col 7-12).**
**Gabarit B — images à gauche (col 1-6), texte à droite (col 8-12).**

Hiérarchie verticale de la colonne de texte, dans cet ordre strict :

| Ordre | Élément | Style | Espacement au-dessus |
|---|---|---|---|
| 1 | **Compteur** `03 / 13` | `.micro`, `--muted` | — |
| 2 | **Kicker rubrique** `DIRECTION ARTISTIQUE` | `.kicker`, `--accent` | 16px |
| 3 | **Titre** | `--t-news`, Unbounded 800, `--ink` | 24px |
| 4 | **Filet** 1px `--line`, largeur `72px` | | 28px |
| 5 | **Contexte** (`contexte_html`) | `.body`, `--ink-2`, `max-width: 62ch` | 28px |
| 6 | **Learning** | `.learning`, `--ink`, précédé d'un filet gauche 2px `--accent` + `padding-left: 20px` | 32px |
| 7 | **Source** `CREATIVE REVIEW ↗` | `.meta`, `--muted` → `--accent` au hover | 32px |

- Le **type** (`actualite` / `pepite`) : quand `type === "pepite"`, ajouter un badge `.micro` `PÉPITE` à droite du compteur, en `--accent-ink` sur aplat `--accent`, `padding: 3px 8px`. C'est **la seule exception** à la règle « un seul aplat d'accent par page », car un seul écran est visible à la fois.
- Le **learning** se termine par un carré plein `6×6px` `--accent`, `display:inline-block`, `margin-left:.5em`, `vertical-align: baseline`.

**Colonne images** — jamais une galerie, toujours une composition :
- **1 image** : plein cadre de la colonne, `aspect-ratio: 4/5`.
- **2 images** : une grande `4/5` + une petite `1/1` décalée de `-15%` verticalement et `+22%` horizontalement, superposition assumée de ~40 px.
- **3-4 images** : une principale `4/5` sur toute la colonne + les autres en bandeau `1/1` sous elle, `grid-template-columns: repeat(3, 1fr)`, `gap: var(--gutter)`. La 4e est ignorée si elle ne rentre pas — **on ne descend jamais en dessous de 100svh à cause des images**.
- Aucune légende visible sauf si l'entrée en fournit une ; sinon `alt` seul.

**Fond des sections :** alterner `--bg` / `--surface` toutes les deux sections (`nth-child(4n+1), nth-child(4n+2)` sur `--bg`, les autres sur `--surface`). Différence de 8 points de luminance : perceptible comme un changement de papier, jamais comme des bandes.

---

## 6. DÉTAILS SIGNATURE

Cinq micro-détails. Ils ne sont pas décoratifs : ce sont eux qui font passer le site de « joli site sombre » à « magazine ».

### 6.1 Le chiffre d'édition en débord

Sur la page édition, `--t-numeral` (jusqu'à 240 px) en `--accent`. Sur l'accueil, le même chiffre en **fantôme** : `color: var(--line-strong)`, taille `--t-block-xl`, positionné en haut à droite du bloc, **débordant de 12 % hors du cadre à droite** (`overflow: hidden` sur le bloc, le chiffre est donc coupé net). Un chiffre coupé par la marge = un magazine imprimé au massicot. Ne jamais le centrer, ne jamais le laisser entier.

### 6.2 Les filets — la discipline du 1px

- **Aucun `border-radius` nulle part dans le système.** Valeur imposée : `0`. Blocs, images, boutons, badges, champs. C'est ce qui donne le tranchant éditorial ; un seul radius de 8 px casse tout.
- Épaisseur : `1px` toujours (`2px` réservé au filet gauche du learning et à l'anneau de focus).
- Couleur : `--line` par défaut, `--line-strong` pour séparer deux sections, `--accent` uniquement pour un état actif.
- Sur écrans HiDPI, ne pas « améliorer » en `0.5px` : le 1px net est voulu.
- Les filets courts (72 px sous un titre de news) s'animent au reveal : `transform: scaleX(0) → scaleX(1)`, origine gauche, `--d-slow var(--ease-edito)`, délai `+140ms` après le titre.

### 6.3 L'index de rubrique latéral

Sur la page édition, ≥ 1200 px : une colonne fixe à droite, `position: fixed; right: clamp(20px,2.4vw,40px); top: 50%; transform: translateY(-50%)`, largeur `12px`.

- Une **graduation** par news : un trait horizontal de `12px × 1px`, `--line-strong`, espacé de `14px`.
- La news **active** : le trait passe à `28px` de large et `--accent`, transition `--d-base var(--ease-out)`, et le **nom de la rubrique** apparaît à sa gauche en `.micro` `--ink-2` (`opacity 0→1`, `translateX(6px)→0`, `--d-fast`).
- Les traits sont cliquables (zone de clic étendue à `32×14px` via un pseudo-élément transparent — cf. §8).
- Disparaît sous 1200 px.

### 6.4 Le compteur de progression

En bas de la page édition, `position: fixed; left: var(--pad-x); bottom: 28px`, `z-index: 40`.

- Format : `03 / 13` en `.micro`, `--muted`, où **le numéro courant est en `--ink`** et le total en `--muted`.
- Sous le compteur, une **barre de 120 px × 1px** en `--line` avec un remplissage `--accent` dont la largeur = progression réelle dans le track. La largeur s'anime en `--d-base var(--ease-out)` à chaque changement de section (pas en continu au scroll — le pas discret est plus magazine que la barre fluide).
- Masqué pendant le hero (fade `--d-base`), apparaît à l'entrée dans `.news-track`.
- Sous 768 px : le compteur reste, la barre disparaît.

### 6.5 Le pied de section « signature d'atelier »

En bas de chaque page, un bandeau de 88 px avec un filet `--line-strong` au-dessus, contenant à gauche `.micro` `VEILLE CRÉATIVE HEBDOMADAIRE`, au centre rien, à droite `.micro` `ÉDITION 03 — 28.08.2026`. Le format de date en pied est **numérique pointé** (`28.08.2026`), alors que le hero utilise le format long français (`VENDREDI 28 AOÛT 2026`). Cette dualité de format est volontaire et systématique : long dans l'éditorial, pointé dans la mécanique.

### 6.6 (bonus) Le curseur de survol de bloc

Sur `@media (hover:hover) and (pointer:fine)` uniquement : au survol d'un bloc d'accueil, un petit disque de `76px` suit le curseur (`translate3d`, `rAF`, jamais `left/top`), fond `--accent`, texte `--accent-ink` en `.micro` : `VOIR`. Apparition `scale(.6)→scale(1)` + `opacity`, `--d-fast var(--ease-out)`. `mix-blend-mode: normal`, pas de difference/exclusion (illisible sur photo). Le curseur natif est masqué (`cursor:none`) **uniquement sur la zone du bloc**. Supprimé si `prefers-reduced-motion`.

---

## 7. RESPONSIVE

### 7.1 Breakpoints

```css
/* mobile first ; les media queries sont toutes en min-width */
--bp-xs:  480px;   /* grand mobile */
--bp-sm:  768px;   /* tablette portrait */
--bp-md:  900px;   /* seuil d'activation du scroll magnétique */
--bp-lg: 1024px;   /* tablette paysage / petit laptop */
--bp-xl: 1280px;   /* desktop — seuil de l'index latéral (1200px) */
--bp-2xl:1600px;   /* large desktop, le conteneur se fige à 1560px */
```

### 7.2 Grille par palier

| Palier | Colonnes | `--pad-x` | Accueil | Page news |
|---|---|---|---|---|
| < 480 | 4 | 20px | 1 colonne, tous les blocs `4/3`, vedette `4/5` | 1 colonne, images sous le texte |
| 480–767 | 4 | 24px | idem, titres +1 cran | idem |
| 768–1023 | 8 | 40px | vedette 8/8 `16/9`, standards 4/8 (2 par ligne) | 1 colonne, images en bandeau 2 colonnes |
| 1024–1279 | 12 | 56px | vedette 12/12 `2/1`, standards 6/12 | 2 colonnes 5+6, gabarits A/B actifs |
| ≥ 1280 | 12 | 72px | nominal (§5.2) | nominal (§5.5) |
| ≥ 1600 | 12 | 72px, conteneur 1560px centré | nominal | nominal |

### 7.3 Dégradation typographique

Les `clamp()` de §2.3 gèrent seuls le redimensionnement. Deux corrections manuelles seulement :

```css
@media (max-width: 767px){
  :root{ --lh-hero: .94; --lh-display: 1.02; }  /* on ré-aère : les grandes tailles serrées ne tiennent pas en petit */
  .hero-title{ letter-spacing:-.02em; }          /* on relâche le serrage optique */
  .kicker, .meta{ letter-spacing:.16em; }        /* .18em coupe les mots longs en petit corps */
}
```

Le **numéro géant** passe de `240px` à `72px` : sur mobile il se place **à gauche du titre, sur sa propre ligne**, et non plus en surtitre débordant.

### 7.4 Ce qui n'existe pas au touch — et son remplacement

Bloc de détection unique, à utiliser partout :

```css
@media (hover: hover) and (pointer: fine){ /* comportements de survol ici */ }
@media (hover: none){ /* alternatives tactiles ici */ }
```

| Comportement desktop | Alternative tactile prescrite |
|---|---|
| **Slideshow au survol des blocs** | **Auto-play à l'entrée dans le viewport.** `IntersectionObserver` à `threshold: 0.6`. Cadence **ralentie à 900 ms** (le cut à 420 ms est illisible sans intention de survol). Seul le **bloc vedette** joue, et sur **3 images** (0→1→2→0). Les blocs standard affichent l'image 0 fixe. L'auto-play s'arrête quand le bloc sort du viewport et ne redémarre pas plus de **2 cycles**. Sous chaque slideshow actif : **5 tirets de 14×1px**, `--line-strong`, l'actif en `--accent` et `24px` de large. |
| **N&B → couleur au hover des images d'articles** | **Images en couleur en permanence** (`filter: contrast(1.03)`). Pas de tap-to-reveal (piège d'affordance). |
| **Curseur `VOIR`** | Supprimé. Remplacé par une flèche `→` statique en bas à droite du bloc, `--muted`. |
| **Scroll magnétique JS** | **Désactivé sous 900px.** On garde `scroll-snap-type: y proximity` + `scroll-snap-align: start` — le navigateur mobile fait un snap natif fluide, et le hijack tactile est le meilleur moyen de rendre une page insupportable au pouce. `scroll-snap-stop: always` est **retiré** en tactile. |
| **Index de rubrique latéral** | Supprimé sous 1200px. Le compteur de progression (§6.4) reste et suffit. |
| **Hover du sommaire (§5.4)** | Lignes empilées, rubrique au-dessus du résumé, filet entre chaque, `→` toujours visible en `--muted`. |
| **Parallax du hero** | Conservé mais amplitude divisée par deux (9 %) ; supprimé sous 768px. |

Toutes les cibles tactiles : **44×44 px minimum** (zone étendue par pseudo-élément si le visuel est plus petit).

### 7.5 Performance

- Zéro framework. Le JS total (slideshow + reveals + scroll assist + index + compteur) doit tenir **sous 9 Ko non minifié**.
- `content-visibility: auto; contain-intrinsic-size: 100svh;` sur `.news-section` — indispensable avec 13 sections plein écran.
- `will-change` uniquement sur `.hero-img` et l'élément de curseur, **jamais** sur les 13 sections.
- Toutes les images d'articles en `loading="lazy"` sauf la première du hero et l'image 0 du bloc vedette.
- Aucune police en `@import`. Aucun CSS bloquant hors la feuille unique inline ou liée.

---

## 8. ACCESSIBILITÉ

### 8.1 Ratios de contraste mesurés (WCAG 2.1, algorithme officiel)

Script de vérification écrit et exécuté le 2026-08-31 (formule officielle : luminance relative sRGB avec linéarisation gamma, ratio `(L1+0.05)/(L2+0.05)`). Les scrims et les états de survol sont composés en alpha avant mesure, pas approximés. Résultats bruts :

```
combinaison                              ratio  seuil  verdict
------------------------------------------------------------------------
--ink sur --bg                          17.49:1    4.5  OK
--ink sur --surface                     16.46:1    4.5  OK
--ink sur --surface-2                   15.19:1    4.5  OK
--ink-2 sur --bg                        10.75:1    4.5  OK
--ink-2 sur --surface                   10.11:1    4.5  OK
--muted sur --bg                         6.14:1    4.5  OK
--muted sur --surface                    5.78:1    4.5  OK
--accent sur --bg                       17.05:1    4.5  OK
--accent sur --surface                  16.04:1    4.5  OK
--accent sur --surface-2                14.81:1    4.5  OK
--bg sur --accent (pastille)            17.05:1    4.5  OK
--ink sur --accent (INTERDIT)            1.03:1    4.5  FAIL   ← combinaison bannie §1.4
--ink sur scrim hero 78%                15.42:1    4.5  OK
--accent sur scrim hero 78%             15.03:1    3.0  OK
--ink-2 sur scrim hero 78%               9.48:1    4.5  OK
--muted sur scrim hero 78%               5.41:1    4.5  OK
--line sur --bg (filet)                  1.35:1    1.0  OK
--line-strong sur --bg                   2.25:1    1.0  OK

--- STRESS : texte sur photo hero N&B claire (haute lumière #DCDCDC) ---
scrim 62% -> #545454 | ink  6.78:1 | ink-2  4.17:1 | muted  2.38:1 | accent  6.61:1
scrim 72% -> #3E3E3E | ink  9.57:1 | ink-2  5.88:1 | muted  3.36:1 | accent  9.33:1
scrim 82% -> #282828 | ink 13.19:1 | ink-2  8.11:1 | muted  4.63:1 | accent 12.86:1

--- hover : accent 8% sur --surface (= --surface-accent #24271A) ---
ink 13.62:1 | muted 4.78:1 | accent 13.28:1
```

**Conclusion : toutes les combinaisons du système passent AA (≥ 4,5:1 texte courant, ≥ 3:1 très grand texte).** Le seul FAIL est `--ink` sur `--accent`, qui est explicitement interdit au §1.4 et n'existe nulle part dans le design — l'unique texte autorisé sur aplat accent est `--accent-ink` (17,05:1).

### 8.2 Corrections imposées par les mesures

Trois règles découlent directement du test de stress, et sont **contraignantes** :

1. **`--muted` est interdit par-dessus toute photo** (2,38:1 à 62 % de scrim). Sur le hero, la date, le numéro d'édition en méta et le `↓ DÉFILER` utilisent **`--ink-2`** (9,48:1 à 78 %) et non `--muted`.
2. **Le scrim minimal sous une zone de texte de hero est de 0,78.** Le dégradé de §3.2 doit atteindre ce seuil sur toute la surface occupée par du texte, pas seulement à sa base. Ajouter le plancher plat `.22` si une photo claire est utilisée.
3. **`--muted` sur `--surface-accent` (état de survol) donne 4,78:1** — au-dessus du seuil, mais avec peu de marge : ne pas descendre `--muted` sous `#93908A`, et ne pas monter `--accent-wash` au-dessus de `.08`.

### 8.3 Règles générales

- **Focus visible partout** : `:focus-visible{ outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 0; }`. Ne jamais supprimer l'outline. Ratio anneau/fond = 17,05:1.
- **Skip link** `Aller au contenu` en premier élément du `<body>`, visible au focus, style `.micro` sur aplat `--accent`.
- **Scroll hijack accessible** : `Tab`, `Home`, `End`, `PageUp/Down`, flèches fonctionnent ; le focus n'est jamais piégé ; aucune section n'est atteignable uniquement par un geste de souris.
- **Structure sémantique** : un seul `<h1>` par page (titre d'édition sur la page édition, nom du site sur l'accueil), chaque news est une `<section>` avec `<h2>`, chaque bloc d'accueil est un `<article>` contenant un `<a>` couvrant.
- **Images** : `alt` descriptif issu du titre de l'entrée pour les images d'articles ; `alt=""` + `role="presentation"` pour les images décoratives de slideshow et le hero (l'information est dans le texte adjacent).
- **Liens externes** : `target="_blank" rel="noopener noreferrer"` + libellé caché `<span class="sr-only"> (nouvel onglet)</span>`.
- **`lang="fr"`** sur `<html>` ; les titres anglais des blocs d'accueil portent `lang="en"` (pour la synthèse vocale).
- **Mouvement** : §4.8 respecté intégralement ; aucune animation ne se répète plus de 3 fois ni ne dure plus de 5 s (WCAG 2.2.2).
- **Zoom** : la page reste utilisable à 200 % ; aucun `user-scalable=no`, `maximum-scale` interdit.
- **Cibles** : 44×44 px minimum au touch (WCAG 2.5.8 largement dépassé).

---

## 9. CHECKLIST DE LIVRAISON

Le développement est conforme si, et seulement si :

- [ ] Aucun `border-radius` ≠ 0 dans la feuille de style.
- [ ] Aucune couleur hors des tokens de §1.2 (grep : pas de hex hors `:root`).
- [ ] Les accents par rubrique des anciens JSON sont ignorés par `build.py`.
- [ ] `--accent` apparaît ≤ 4 fois par écran, jamais sur une photo, jamais en paragraphe.
- [ ] Aucun texte en full caps sans `letter-spacing ≥ .14em`.
- [ ] Unbounded n'est jamais en `text-transform: uppercase`.
- [ ] Le grain (couche A) est présent sur toutes les pages, la couche B uniquement sur les heroes.
- [ ] Le slideshow est en **cut** (transition 90 ms), pas en crossfade.
- [ ] `prefers-reduced-motion` neutralise slideshow, parallax, hijack, reveals et curseur.
- [ ] Le scroll magnétique est désactivé sous 900 px et remplacé par `scroll-snap: proximity`.
- [ ] Les images d'articles sont en couleur permanente sous `@media (hover:none)`.
- [ ] `100svh` partout où un plein écran est demandé (jamais `100vh`).
- [ ] `content-visibility: auto` sur les sections de news.
- [ ] Focus visible sur 100 % des éléments interactifs.
- [ ] Aucune combinaison texte/fond sous 4,5:1 (§8.1).
