#!/usr/bin/env bash 
INGULARITYENV_MYOPT="SIMD" singularity build --force --fakeroot airl_env_tensorflow.sif airl_env_tensorflow.def
