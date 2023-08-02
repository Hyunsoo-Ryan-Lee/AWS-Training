#!/bin/bash

echo "WHAT APP DO YOU WANT TO START? ENTER THE NUMEBER"
echo "1. LOTTERY SITE"
echo "2. MEMORY GAME"
echo "3. AWS FILE UPLOADER"

read app

if [ $app == "1" ]; then
	echo "LOTTERY SITE START!"
    source /home/ubuntu/AWS-Training/Flet/flet/bin/activate
    flet run -w /home/ubuntu/AWS-Training/Flet/lottery-site/flet_main.py
elif [ $app == "2" ]; then
	echo "MEMORY GAME START!"
    source /home/ubuntu/AWS-Training/Flet/flet/bin/activate
    flet run -w /home/ubuntu/AWS-Training/Flet/memory-game/flet_main.py
elif [ $app == "3" ]; then
	echo "AWS FILE UPLOADER START!"
    source /home/ubuntu/AWS-Training/Flet/flet/bin/activate
    flet run -w /home/ubuntu/AWS-Training/Flet/photo-uploader/flet_main.py
else
	echo "WRONG NUMBER!"
fi