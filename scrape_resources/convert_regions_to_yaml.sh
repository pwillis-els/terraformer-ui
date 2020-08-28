#!/bin/sh
set -e -u

if [ $# -lt 2 ] ; then
    echo "Usage: $0: FILE RESOURCE_TYPE"
    echo ""
    echo "Example:"
    echo "   $0 aws_regions.txt aws > aws_regions.yaml"
    exit 1
fi

FILE="$1"; shift
RESOURCE="$1"; shift

BN="`basename "$FILE"`"

printf "regions:\n  $RESOURCE:\n"

cat "$FILE" | \
    sed -e 's/^/    - /g'

