#!/bin/zsh

echo "Checking quality of backend python code with pyflakes."
for f in `ls backend/*.py`
do
    pyflakes-2.7 $f
done
echo "Done."
