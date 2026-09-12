#!/bin/sh
# Publie la veille créative : régénère le site puis pousse sur GitHub.
# Le déploiement se déclenche tout seul à la réception.
# Usage : sh publier.sh
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
REPO="krlpz-dev/veille"
CLONE="$HOME/.cache/veille-publication"
cd "$SRC"

echo "→ Génération de toutes les éditions"
for f in data-*.json; do
  python3 build.py "$f" ./ >/dev/null
done
mkdir -p docs
cp index.html docs/
cp veille-*.html docs/
echo "   $(ls docs/veille-*.html | wc -l | tr -d ' ') éditions dans docs/"

TOKEN=$(tr -d '\n\r ' < "$SRC/.secrets/github-token")
if [ -z "$TOKEN" ]; then
  echo "Jeton GitHub absent : .secrets/github-token"
  exit 1
fi
URL="https://x-access-token:$TOKEN@github.com/$REPO.git"

if [ -d "$CLONE/.git" ]; then
  git -C "$CLONE" fetch -q "$URL" main
  git -C "$CLONE" reset -q --hard FETCH_HEAD
else
  mkdir -p "$(dirname "$CLONE")"
  git clone -q "$URL" "$CLONE"
fi

echo "→ Préparation de l'envoi"
rm -rf "$CLONE/docs"
mkdir -p "$CLONE/docs"
cp "$SRC"/docs/*.html "$CLONE/docs/"
cp "$SRC"/data-*.json "$SRC"/editions-passees.json "$SRC"/build.py "$SRC"/netlify.toml "$SRC"/.gitignore "$SRC"/README.md "$SRC"/DA-SPEC.md "$SRC"/publier.sh "$CLONE/"

cd "$CLONE"
git config user.email "petzold.karl@gmail.com"
git config user.name "Karl Petzold"
git add -A
if git diff --cached --quiet; then
  echo "→ Rien de nouveau, le site en ligne est déjà à jour."
  exit 0
fi
git commit -q -m "Veille du $(date +%Y-%m-%d)"
git push -q "$URL" HEAD:main
echo "→ Envoyé sur github.com/$REPO. Le site se met à jour en une à deux minutes."
