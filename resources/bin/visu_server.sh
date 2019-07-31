#!/bin/bash

xinit_pid=""
x11vnc_pid=""
novnc_pid=""

cleanup() {
    trap - TERM QUIT INT EXIT
    trap "true" CHLD   # Ignore cleanup messages                                                                                                                                                    
    echo
    if [ -n "${novnc_pid}" ]; then
        echo "Terminating novnc (${novnc_pid})"
        kill ${novnc_pid}
    fi
    if [ -n "${x11vnc_pid}" ]; then
        echo "Terminating x11vnc (${x11vnc_pid})"
        kill ${x11vnc_pid}
    fi
    if [ -n "${xinit_pid}" ]; then
        echo "Terminating xinit (${xinit_pid})"
        pkill -15 Xorg
	sleep 1
    fi
}
trap "cleanup" TERM QUIT INT EXIT

echo "Starting services for VISU_server"

echo "Starting Xinit (xdummy)"
xinit -- :0 -nolisten tcp vt$XDG_VTNR -noreset +extension GLX +extension RANDR +extension RENDER +extension XFIXES &> /opt/xinit.log &
xinit_pid="$!"
sleep 0.1
if ! ps -p ${xinit_pid} >/dev/null; then
    xinit_pid=
    echo "Failed to start xinit (xdummy)"
    exit 1
fi

echo "Starting X11vnc"
x11vnc -display :0 -forever -shared -nopw  &> /opt/x11vnc.log &
x11vnc_pid="$!"
sleep 0.1
if ! ps -p ${x11vnc_pid} >/dev/null; then
    x11vnc_pid=
    echo "Failed to start x11vnc"
    exit 1
fi


echo "Starting novnc"
cd /opt/noVNC
bash -c "./utils/launch.sh "  &> /opt/novnc.log &
novnc_pid="$!"
cd - &>/dev/null
sleep 0.1
if ! ps -p ${novnc_pid} >/dev/null; then
    novnc_pid=
    echo "Failed to start noVNC"
    exit 1
fi

wait

echo "Wait for cleanup"
sleep 2
echo "finished"
