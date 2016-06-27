#!/bin/bash 

for F in multiprocessing_names.py mp_*.py ; do 
    python $F > /dev/null
    STATUS=$?
    if [[ $STATUS != 0 ]]; then exit 1; fi
    echo $F '->' $STATUS
done
