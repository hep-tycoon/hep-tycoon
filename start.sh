#/bin/bash

DEBUG=0
if [[  $# > 0 && $1 = "--debug" ]]; then
    DEBUG=1
    URL="/init_game/linear/ee/$USER"
fi

# clean up before
rm backend/*.pyc

# beta (todo: find the correct python version)
(sleep 2 && open "http://localhost:5000$URL") &
echo "Gameserver starting. Stop with ctrl-c."
python2.7 testserver.py $DEBUG
