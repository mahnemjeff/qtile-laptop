#! /bin/bash
nitrogen --restore &
picom &
lxpolkit &
dunst &
~/.config/qtile/scripts/check_battery.sh &
setxkbmap -option caps:escape
