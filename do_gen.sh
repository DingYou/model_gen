#!/usr/bin/env bash

pymysql_version=$(pip3 list | grep -i pymysql | awk '{print $2}')
if [ "$pymysql_version" ]; then
  echo "PyMySQL version is $pymysql_version"
else
  pip3 install pymysql
fi

current_path=$(pwd)
cd "$(dirname "$0")" && python3 class_gen.py
cd "$current_path" || exit 1