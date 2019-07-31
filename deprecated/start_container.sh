LOCAL_EXP_PATH=~/'git'
IMAGENAME='aneoshun/airl_env:latest'
CONTAINERNAME="airl_env_$USER"
NOVNC_IP=6081


while getopts d flag
do
    case $flag in
	
        d)
            echo Display on
	    V_DISPLAY=true
            ;;
        ?)
            exit
            ;;
    esac
done
#shift $(( OPTIND - 1 ))  # shift past the last flag or argument

echo "Visualisation available after activating the visu_server.sh script at the http://localhost:$NOVNC_IP/"
if [ ! "$(docker ps -q -f name=^/$CONTAINERNAME)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=^/$CONTAINERNAME)" ]; then
        docker start -ai $CONTAINERNAME
    else
	docker run --privileged --name=$CONTAINERNAME -p $NOVNC_IP:6080 -m 8GB -it  -v $LOCAL_EXP_PATH:/git/sferes2/exp  $IMAGENAME
    fi
fi
