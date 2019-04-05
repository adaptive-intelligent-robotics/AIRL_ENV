LOCAL_EXP_PATH=~/'git'
IMAGENAME='aneoshun/airl_env:dart_exp_graphic_test'
CONTAINERNAME='airl_env'

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


if [ ! "$(docker ps -q -f name=^/$CONTAINERNAME)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=^/$CONTAINERNAME)" ]; then
        docker start -ai airl_env
    else
	if [ "$V_DISPLAY" = true ] ; then
	    xhost + 127.0.0.1
	    xhost local:root
	    docker run --privileged --name=$CONTAINERNAME -e DISPLAY=host.docker.internal:0 -m 8GB -it $IMAGENAME
	else
            docker run --privileged --name=$CONTAINERNAME -m 8GB -it -v /tmp/.X11-unix:/tmp/.X11-unix $IMAGENAME
	fi

    fi
fi


#=host.docker.internal:0