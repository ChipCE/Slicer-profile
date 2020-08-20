#!/bin/bash

WDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$WDIR"

echo "Removing current backup..."
rm -rf cura
echo "Creating new profiles backup..."
cp -r ~/.local/share/cura cura
echo "Done"
exit 0