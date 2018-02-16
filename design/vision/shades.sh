#!/bin/bash
cd /home/pi/ || exit #move to correct directory
export DISPLAY=:0.0
python shades.py #start application
