#!/bin/bash

# build.sh will build a Singularity container. It's not overly complicated.
#
# USAGE: build.sh --uri collection-name/container-name --cli registry Singularity
#        build.sh --uri collection-name/container-name --cli registry
#        build.sh Singularity

# Copyright (C) 2017-2018 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -o errexit
set -o nounset

function usage() {

    echo "USAGE: build [recipe] [options]"
    echo ""
    echo "OPTIONS:

          Image Format
              --uri   -u    if uploading, a uri to give to sregistry
              --cli   -c    the sregistry client to use (if uploading)
              --help  -h    show this help and exit
              "
}

# --- Option processing --------------------------------------------------------

uri=""
cli=""
tag=""
imagefile=""
while true; do
    case ${1:-} in
        -h|--help|help)
            usage
            exit 0
        ;;
        -u|--uri)
            shift
            uri="${1:-}"
            shift
        ;;
        -t|--tag)
            shift
            tag="${1:-}"
            shift
        ;;
        -k|--token)
            shift
            token="${1:-}"
            shift
        ;;
        -c|--cli)
            shift
            cli="${1:-}"
            shift
        ;;
        -i|--imagefile)
            shift
	    echo "imagefile provided"
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

################################################################################
### Image File ################################################################
################################################################################

	
echo ""
echo "Image file: ${imagefile}"


################################################################################
### Storage Client #############################################################
################################################################################

is_valid_client () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

# Test if client is valid

clients=("ghcr")

if [ "${cli}" != "" ]; then
    is_valid_client "${cli}" "${clients[@]}"
    if [ $? -ne 0 ]; then
        echo "${cli} is not a valid choice! Choose from ${clients[@]}";
        exit 1
    fi
    echo "Storage Client: ${cli}"
else
    echo "Storage Client: none"
fi


################################################################################
### UPLOAD! #####################################################################
################################################################################

if [ -f "${imagefile}" ]; then

    # Example testing using run (you could also use test command)

    # echo "Testing the image... Marco!"
    # singularity exec $imagefile echo "Polo!"

    # Example sregistry commands to push to endpoints
    
    if [ "${cli}" != "" ]; then
	
        # If the uri isn't provided, he gets a robot name
        if [ "${uri}" == "" ]; then
            uri=$(python -c "from sregistry.logger.namer import RobotNamer; bot=RobotNamer(); print(bot.generate())")
        fi
	
        # If a tag is provided, add to uri
        if [ "${tag}" != "" ]; then
            uri="${uri}:${tag}"
        fi
	
 	#echo "Adding key"
	#apptainer key import $SREGISTRY_KEY

	#echo "Signing container"
	#apptainer sign "${imagefile}"
	
	echo "Login to remote"
	apptainer remote add --no-login ghcr oras://ghcr.io
	echo $token
	apptainer remote login -u aneoshun --password $token ghcr
	apptainer push "${imagefile}" "${uri}" 
	
	
    else
        echo "Skipping upload. Image $imagefile is finished!"
    fi
    
else

    echo "Singularity image ${imagefile} not found!"
    exit 1

fi
