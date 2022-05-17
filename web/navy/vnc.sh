#!/bin/bash
# entrypoint.sh file for starting the xvfb with better screen resolution, configuring and running the vnc server, pulling the code from git and then running the test.
export DISPLAY=:0
Xvfb :0 -screen 0 1366x768x16 &
x11vnc -passwd TestVNC -display :0 -N -forever &
google-chrome
wait