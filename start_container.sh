LOCAL_EXP_PATH='/Users/antoinecully/git'
IMAGENAME='airl_env' #aneoshun/airl_env:dart'
CONTAINERNAME='airl_env'

if [ ! "$(docker ps -q -f name=^/$CONTAINERNAME)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=^/$CONTAINERNAME)" ]; then
        docker start -ai airl_env
    else
        docker run --name=$CONTAINERNAME -m 8GB -it -v $LOCAL_EXP_PATH:/git/sferes2/exp $IMAGENAME
    fi
fi