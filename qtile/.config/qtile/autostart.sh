#!/bin/bash
xrandr --output eDP1 --auto --output HDMI1 --auto --right-of eDP1 &

feh --bg-fill /usr/share/backgrounds/kali-16x9/kali-red-sticker.jpg &
feh --bg-fill /usr/share/backgrounds/kali-16x9/kali-red-sticker.jpg --no-xinerama --screen eDP1 &
feh --bg-fill /usr/share/backgrounds/kali-16x9/kali-red-sticker.jpg --no-xinerama --screen HDMI1 &
sleep 2s && picom &

barrier &


