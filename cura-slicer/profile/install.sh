#!/bin/bash

WDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$WDIR"

echo "Removing current config..."
rm -rf ~/.local/share/cura
echo "Installing profiles..."
cp -r ./cura ~/.local/share/cura/
echo "Done"
exit 0