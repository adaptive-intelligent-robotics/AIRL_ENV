#!/bin/bash

turbovnc_pid=""
novnc_pid=""

cleanup() {
    trap - TERM QUIT INT EXIT
    trap "true" CHLD   # Ignore cleanup messages                                                                                                                                                    
    echo
    if [ -n "${novnc_pid}" ]; then
        echo "Terminating novnc (${novnc_pid})"
        kill ${novnc_pid}
    fi
    if [ -n "${turbovnc_pid}" ]; then
        echo "Terminating turbovnc (${turbovnc_pid})"
        #kill ${turbovnc_pid}
    fi
}
trap "cleanup" TERM QUIT INT EXIT

echo "Starting services for VISU_server"


echo "Starting TurboVNC"
/opt/TurboVNC/bin/vncserver  &> /opt/turbovnc.log &
turbovnc_pid="$!"
echo $turbovnc_pid
sleep 0.1
if ! ps -p ${turbovnc_pid} >/dev/null; then
    turbovnc_pid=
    echo "Failed to start turbovnc"
    exit 1
fi

sleep 1
str=$(cat /opt/turbovnc.log |grep "display unix:" )
value=${str#*"display unix:"}
port_novnc=$((6080+$value))
port_turbovnc=$((5900+$value))



echo "Starting novnc"
cd /opt/noVNC
bash -c "./utils/launch.sh --listen $port_novnc --vnc localhost:$port_turbovnc "  &> /opt/novnc.log &
novnc_pid="$!"
cd - &>/dev/null
sleep 0.1
if ! ps -p ${novnc_pid} >/dev/null; then
    novnc_pid=
    echo "Failed to start noVNC"
    exit 1
fi


echo "Please do: export DISPLAY=\":$value\""
echo "you can access the visualisation server at localhost:$port_novnc"

if [ "$#" -eq 0 ]
then
    wait
else
    sleep 2
    cleanup
fi

echo "Wait for cleanup"
sleep 2
echo "finished"


exit 0
