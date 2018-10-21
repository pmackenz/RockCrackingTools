#!/usr/bin/bash

DELAY=25

convert -delay $DELAY sdir015cm*png anim_sdir015cm.gif
convert -delay $DELAY sdir020cm*png anim_sdir020cm.gif
convert -delay $DELAY sdir025cm*png anim_sdir025cm.gif
convert -delay $DELAY sdir030cm*png anim_sdir030cm.gif
convert -delay $DELAY sdir050cm*png anim_sdir050cm.gif
