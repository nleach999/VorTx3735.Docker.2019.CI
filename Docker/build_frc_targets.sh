#!/bin/bash


mkdir -p $CODEBUILD_SRC_DIR/logs
chmod +x $CODEBUILD_SRC_DIR/gradlew

set -o pipefail

$CODEBUILD_SRC_DIR/gradlew $@ 2>&1 | tee $CODEBUILD_SRC_DIR/logs/build.log

if [ "$?" -ne "0" ]; then
    log_to_slack $CODEBUILD_SRC_DIR/logs/build.log
    exit 1
fi