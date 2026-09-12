#!/bin/sh
cd "$(dirname "$0")" || exit 1
sh publier.sh
echo ""
echo "Terminé. Vous pouvez fermer cette fenêtre."
