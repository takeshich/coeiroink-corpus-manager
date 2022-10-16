#!/bin/bash

FILENAME=./mana-corpus-processed-by-mycoeiroink.txt
EOL=$(cat ${FILENAME} | wc -l)
cat ${FILENAME} |awk -v step=5 -v eol=${EOL} '{for (i=3;i<=eol;i+=step){ if(NR==i) print $0}}'
