#!/bin/bash
cd /home/pi/ || exit #move to correct directory
export DISPLAY=:0.0
echo 'yes' > run.txt
while [ "$(cat run.txt)" == 'yes' ]; do
  python telegrambot.py #start application
done
