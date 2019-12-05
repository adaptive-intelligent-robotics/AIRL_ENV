#!/usr/bin/env bash


# --- Option processing --------------------------------------------------------
imagefile=""
while true; do
    case ${1:-} in
        --nofakeroot) nofakeroot=true
            shift
        ;;
        -i|--imagefile)
            shift
            imagefile="${1:-}"
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
    


