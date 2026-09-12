#!/bin/sh
# Publie la veille créative : régénère le site puis pousse sur GitHub.
# GitHub déclenche ensuite le déploiement automatique.
# Usage : sh publier.sh
cd "$(dirname "$0")" || exit 1
REPO="krlpz-dev/veille"

echo "→ Génération de toutes les éditions"
for f in data-*.json; do
  python3 build.py "$f" ./ >/dev/null || exit 1
done
mkdir -p docs
cp index.html docs/
cp veille-*.html docs/
echo "   $(ls docs/veille-*.html | wc -l | tr -d ' ') éditions dans docs/"

TOKEN=$(tr -d '\n\r ' < .secrets/github-token 2>/dev/null)
if [ -z "$TOKEN" ]; then
  echo "Jeton GitHub absent : .secrets/github-token"
  exit 1
fi

if [ ! -d .git ]; then
  echo "→ Initialisation du dépôt"
  git init -q
  git symbolic-ref HEAD refs/heads/main
fi
git config user.email "petzold.karl@gmail.com"
git config user.name "Karl Petzold"

echo "→ Envoi sur github.com/$REPO"
git add -A
git commit -q -m "Veille du $(date +%Y-%m-%d)" 2>/dev/null || echo "   rien de nouveau à committer"
git push -q "https://x-access-token:$TOKEN@github.com/$REPO.git" HEAD:main || exit 1
echo "→ Envoyé. Le déploiement se lance tout seul, comptez une à deux minutes."
