#!/usr/bin/env bash
python3 -m FridgeBot > /dev/null 2>&1 &
echo "Started bot"
while [[ 1 ]]
do
    python3 -m pip list --index-url http://Paz:8080/simple fridgebot --trusted-host Paz --outdated | grep 'FridgeBot' > /dev/null
	if [[ $? == 0 ]]; then
		pkill -SIGKILL python3
		if pgrep -x "python3" > /dev/null
        then
            continue
        fi

		echo "Updating"
		python3 -m pip install -U --index-url http://Paz:8080/simple fridgebot --trusted-host Paz
		echo "Running updated version"
		python3 -m FridgeBot > /dev/null 2>&1 &

	fi
	
	sleep 5
done
