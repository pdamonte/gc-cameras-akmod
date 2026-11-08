#!/usr/bin/env bash
# Build akmod-gc-cameras + gc-cameras RPMs into ./rpmbuild/RPMS
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V=0.2
TOP="$ROOT/rpmbuild"
rm -rf "$TOP"; mkdir -p "$TOP"/{SOURCES,SPECS}
tar -C "$ROOT/src" -czf "$TOP/SOURCES/gc-cameras-$V.tar.gz" "gc-cameras-$V"
cp "$ROOT"/extra/*.conf "$TOP/SOURCES/"
cp "$ROOT"/SPECS/*.spec "$TOP/SPECS/"
rpmbuild --define "_topdir $TOP" -ba "$TOP/SPECS/gc-cameras.spec"
rpmbuild --define "_topdir $TOP" -ba "$TOP/SPECS/gc-cameras-kmod.spec"
find "$TOP/RPMS" -name '*.rpm' -print
