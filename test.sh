#!/usr/bin/env bash
# shellcheck disable=SC1091
source version.sh
tox -- --junitxml="${PACKAGE}.xml"
