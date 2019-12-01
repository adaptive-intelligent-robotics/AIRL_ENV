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


echo "==== TEST IMAGE ===="
singularity build --sandbox $build_option test_env airl_env_base.sif
singularity test -w test_env
echo "==== DONE TEST IMAGE ===="

ret=$?
exit $ret


