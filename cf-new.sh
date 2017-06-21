#!/usr/bin/env bash

PROB=$1
REGEX="([1-9][0-9]*)([A-Za-z][A-Za-z0-9]*)"

if [[ $PROB =~ $REGEX ]]; then
  CONTEST=${BASH_REMATCH[1]}
  SEQ=${BASH_REMATCH[2]}
  mkdir -p $CONTEST
  cd $CONTEST && vim $PROB.cpp
else
  echo "$PROB does not match"
fi

