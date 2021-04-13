#!/usr/bin/env bash

./build_image_without_ci.sh --basename airl_env_base
./build_image_without_ci.sh --basename airl_env_torch
./build_image_without_ci.sh --basename airl_env_bare

