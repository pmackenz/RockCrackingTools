#!/bin/bash

DELAY=25

for SIZE in 015 020 025 030 040 050 062 075 087 100 125 150 200 300 500
do
    INFILES=sigma-dir-${SIZE}cm\*png
    OUTFILE=anim_sigma-dir-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=dir-${SIZE}cm\*png
    OUTFILE=anim_dir-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=top10-${SIZE}cm\*png
    OUTFILE=anim_top10-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=sdir-${SIZE}cm\*png
    OUTFILE=anim_sdir-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=DBLE-sdir-top10-dir${SIZE}cm\*png
    OUTFILE=anim_DBLE-sdir-top10-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi

    INFILES=DBLE-dev-mean-dir${SIZE}cm\*png
    OUTFILE=anim_DBLE-dev-mean-${SIZE}cm.gif
    if [ ! -f ${OUTFILE} ]
    then
        convert -delay ${DELAY} ${INFILES} ${OUTFILE}
    fi
done
