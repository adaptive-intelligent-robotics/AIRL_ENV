LOCAL_EXP_PATH=~/'git'
IMAGENAME='aneoshun/airl_env:dart_exp_ready'
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
	    docker run --name=$CONTAINERNAME -e DISPLAY=host.docker.internal:0 -m 8GB -it -v $LOCAL_EXP_PATH:/git/sferes2/exp $IMAGENAME
	else
            docker run --name=$CONTAINERNAME -m 8GB -it -v $LOCAL_EXP_PATH:/git/sferes2/exp $IMAGENAME
	fi

    fi
fi
