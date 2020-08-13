#!/usr/bin/env bash

current_path=`pwd`
cd "$(dirname "$0")" && python3 class_gen.py
cd "$current_path" || exit 1