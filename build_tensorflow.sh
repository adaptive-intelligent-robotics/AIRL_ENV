#!/usr/bin/env bash

# idiomatic parameter and option handling in sh
while test $# -gt 0
do
    case "$1" in
        --nofakeroot) nofakeroot=true
            ;;
        --*) echo "bad option $1"
            ;;
        *) echo "argument $1"
            ;;
    esac
    shift
done

build_option=""
if [ "$nofakeroot" != true ]; then
    echo "using FAKEROOT"
    build_option="--fakeroot"
fi


python3 airl_env_tensorflow.py > hppcm_airl_env_tensorflow.def
ret=$?
if [ $ret -ne 0 ]; then
    echo "Generation of the definition file failed."
    exit $ret
fi

cat hppcm_airl_env_tensorflow.def

singularity build --notest $build_option airl_env_tensorflow.sif hppcm_airl_env_tensorflow.def

ret=$?
exit $ret
