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

if [ $# == 0 ] ; then
    imagefile="airl_env_base.sif"
else
    imagefile=$1
fi

echo ""
echo "Image file: ${imagefile}"


if [ -f "${imagefile}" ]; then
    echo "==== TEST IMAGE ===="
    singularity build --sandbox $build_option test_env_${imagefile} ${imagefile}
    singularity test -w test_env_${imagefile}
    echo "==== DONE TEST IMAGE ===="
    ret=$?
    exit $ret

else

    echo "Singularity image ${imagefile} not found!"
    exit 1

fi
    


