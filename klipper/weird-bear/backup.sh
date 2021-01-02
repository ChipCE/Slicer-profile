#/bin/bash

# move to script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
# remove old files
rm *.cfg >/dev/null 2>&1
# copy over
yes | cp ~/klipper_config/*.cfg .
echo "Done!"
