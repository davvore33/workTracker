#!/usr/bin/env bash
    echo $1 $2
    cd "$1"
    mkdir ./workTracker_tmp
    mv $2 ./workTracker_tmp/
    cd ./workTracker_tmp/
    echo pwd `pwd`
#    pdflatex -synctex=1 -interaction=nonstopmode $2 -output-directory="$1"
    lualatex -synctex=1 -interaction=nonstopmode $2 -output-directory="$1"
    mv *.pdf ../
    cd ../
    rm -rf workTracker_tmp/