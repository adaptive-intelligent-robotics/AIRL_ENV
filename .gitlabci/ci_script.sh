#!/usr/bin/env bash

# --- Option processing --------------------------------------------------------
tag=""

while true; do
    case ${1:-} in
        -t|--tag)
            shift
            tag="${1:-}"
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


if [ $# == 0 ] ; then
    basename="airl_env_base"
else
    basename=$1
fi

/bin/bash ./.gitlabci/build_image.sh $basename --nofakeroot 
/bin/bash ./.gitlabci/test_image.sh $basename.sif --nofakeroot 
if [ $CI_COMMIT_REF_NAME = "master" ]; then /bin/bash ./.gitlabci/push_image.sh --uri library://airl_lab/default/airl_env --tag $tag --cli registry --imagefile $basename.sif  ; else echo "NOT on master branch, not pushing"; fi; 
