#/bin/bash

# clean up before
rm backend/*.pyc

# beta (todo: find the correct python version)
(sleep 2 && open "http://localhost:5000$1") &
echo "Gameserver starting. Stop with ctrl-c."
python2.7 testserver.py
