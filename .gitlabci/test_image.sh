#!/usr/bin/env bash


# --- Option processing --------------------------------------------------------

while true; do
    case ${1:-} in
        --nofakeroot) nofakeroot=true
            shift
        ;;
        \?) printf "illegal option: -%s\n" "${1:-}" >&2
            usage
            exit 1
        ;;
        -*)
            printf "illegal option: -%s\n" "${1:-}" >&2
            usage
            exit 1
        ;;
        *)
            break;
        ;;
    esac
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
    


