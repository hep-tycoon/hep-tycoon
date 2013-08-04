#/bin/bash

# beta (todo: find the correct python version)
(sleep 2 && open http://localhost:5000) &
echo "Gameserver starting. Stop with ctrl-c."
python2.7 testserver.py
