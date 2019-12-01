#!/usr/bin/env bash

python3 airl_env_base.py > hppcm_airl_env_base.def
cat hppcm_airl_env_base.def
singularity build --notest --fakeroot hppcm_airl_env_base.sif hppcm_airl_env_base.def

