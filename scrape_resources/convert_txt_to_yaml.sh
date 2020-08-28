#!/bin/sh
set -e -u

if [ $# -lt 2 ] ; then
    echo "Usage: $0: FILE RESOURCE_TYPE"
    echo ""
    echo "Example:"
    echo "   $0 aws_resources_from_readme.txt aws > aws_resources.yaml"
    exit 1
fi

FILE="$1"; shift
RESOURCE="$1"; shift

BN="`basename "$FILE"`"

printf "resources:\n  $RESOURCE:\n"

cat "$FILE" | \
    sed -e 's/^    \([^ ]\+\)/    \1:/g' | \
    sed -e 's/(/# (/g' | \
    sed -e 's/^        /      - /g'

#    sed -e 's/^    \([^ ]\+\)/  - \1:/g' | \
