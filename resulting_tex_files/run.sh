#!/usr/bin/env bash
set -e

MAIN=$1
BUILDDIR="build"

mkdir -p "$BUILDDIR"

pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILDDIR" "$MAIN"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILDDIR" "$MAIN"
