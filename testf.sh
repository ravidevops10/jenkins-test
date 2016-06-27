#!/bin/bash 

for F in mpfail.py ; do 
    python $F > /dev/null
    STATUS=$?
    if [[ $STATUS != 0 ]]; then exit 1; fi
    echo $F '->' $STATUS
done
