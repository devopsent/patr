#!/usr/bin/env bash
# shellcheck disable=SC1091
source version.sh
python ./setup.py bdist_wheel
pushd "${PWD}"
cd dist || {
    echo "FAILURE: cannot chdir to dist";
    exit 1;
}
dir2pi --no-symlink .
popd
