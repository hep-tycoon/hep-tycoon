#!/bin/zsh

echo "Checking quality of backend python code with pyflakes."
for f in `ls backend/*.py`
do
    pyflakes-2.7 $f
done
echo "Done."

echo "Checking quality of frontend javascript code with jslint."
for f in `find . -name "*.js" -not -name "*.min.js"`
do
    echo $f
    jslint $f
done
echo "Done."
