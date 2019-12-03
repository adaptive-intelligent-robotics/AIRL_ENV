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
    basename="airl_env_base"
else
    basename=$1
fi


python3 $basename.py > $basename.def
ret=$?
if [ $ret -ne 0 ]; then
    echo "Generation of the definition file failed."
    exit $ret
fi

cat $basename.def

singularity build --notest $build_option $basename.sif $basename.def

ret=$?
exit $ret
