#!/bin/bash

set -eu

cd "$1/share/template"
mkdir -p wizard

echo "Process templates in $1/share/template"

ls | grep -v wizard |
while
    read I
do
    echo $I
    cp -afl $I/wizard/bitmap wizard/
    rm -rf $I/wizard/bitmap
    ln -sf ../../wizard/bitmap $I/wizard/bitmap

    if [ -d $I/wizard/letter/$I ]; then
        mv -f $I/wizard/letter/$I ${I}_wizard_letter_${I}
        rm -rf $I/wizard/letter/*
        mv -f ${I}_wizard_letter_${I} $I/wizard/letter/$I
    else
        rm -rf $I/wizard/letter/*
    fi
done
echo "done"

