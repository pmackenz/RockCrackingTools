#!/bin/bash

DELAY=25

for SIZE in 015 020 025 030 040 050 062 075 087 100 125 150 200 300 500
do
    INFILES=dir${SIZE}cm\*png
    OUTFILE=anim_dir${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=sdir${SIZE}cm\*png
    OUTFILE=anim_sdir${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi
done
