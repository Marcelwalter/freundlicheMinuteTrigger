#! /bin/bash

echo Hello World

echo -n -e "\033]0;Companionscript\007"

osascript -e 'tell application "Terminal" to close (every window whose name contains "Companionscript")' &

exit 0