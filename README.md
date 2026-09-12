# Veille créative hebdomadaire

Site statique généré par `build.py` (Python 3, bibliothèque standard uniquement).
Le dossier `docs/` est la sortie publiée. Chaque push sur `main` redéploie le site.

URL : https://veille-karlpetzold.netlify.app

## Structure

```
data-AAAA-MM-JJ.json   contenu d'une édition (meta + treize entrées)
editions-passees.json  éditions dont le data n'est plus dans le dossier, pour la numérotation
build.py               génère la page d'une édition et régénère l'accueil
docs/                  sortie publiée, commitée telle quelle
DA-SPEC.md             parti pris graphique de référence
.secrets/github-token  jeton GitHub, hors dépôt
```

## Publier

```
sh publier.sh
```

Le script régénère toutes les pages, met `docs/` à jour, commit et pousse.
Double-cliquer `PUBLIER.command` dans le Finder fait la même chose.

## Ajouter une édition à la main

1. Déposer `data-AAAA-MM-JJ.json` dans le dossier.
2. `sh publier.sh`

Le numéro d'édition est recalculé tout seul dans l'ordre chronologique, ne pas le fixer dans le fichier.

## Schéma d'une édition

```json
{
  "date": "AAAA-MM-JJ",
  "meta": {
    "title_en": "TITRE COURT EN ANGLAIS",
    "deck_en": "2 à 3 lignes sur les trois news les plus fortes",
    "highlights": ["trois phrases courtes"],
    "topics_fr": ["treize formules très courtes, dans l'ordre des rubriques"],
    "hero_image": "URL absolue",
    "hero_credit": "Image générée pour cette édition"
  },
  "intro": "une ou deux phrases",
  "entrees": [
    {
      "rubrique": "direction-artistique",
      "titre": "...",
      "type": "actualite",
      "source_nom": "...",
      "source_url": "...",
      "images": ["..."],
      "contexte_html": "...",
      "learning": "une phrase"
    }
  ]
}
```

Rubriques, dans l'ordre : direction-artistique, mode, luxe, craft, architecture, scenographie, photographie, film, fantasy, gaming, ui, ia, philosophie.
