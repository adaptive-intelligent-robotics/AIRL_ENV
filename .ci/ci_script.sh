#!/usr/bin/env bash

# --- Option processing --------------------------------------------------------
tag=""
basename=""
while true; do
    case ${1:-} in
        -t|--tag)
            shift
            tag="${1:-}"
            shift
        ;;
        -b|--basename)
            shift
            basename="${1:-}"
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

echo "basename:"
echo $basename
echo "tag:"
echo $tag

/bin/bash ./.ci/build_image.sh --basename $basename --nofakeroot 
# /bin/bash ./.ci/test_image.sh --imagefile $basename.sif --nofakeroot 
#if [ $CI_COMMIT_REF_NAME = "master" ]; then 
/bin/bash ./.ci/push_image.sh --uri library://adaptive-intelligent-robotics/AIRL_ENV --tag $tag --cli ghcr --imagefile $basename.sif  #; else echo "NOT on master branch, not pushing"; fi; 
