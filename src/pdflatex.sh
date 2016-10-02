#!/usr/bin/env bash
mkdir /tmp/workTracker/
cd /tmp/workTracker/
args=${@}
for N in ${args[@]};
do
#    if [[N == 'pdflatex.sh' || N == '' ]]; then
#        break
#    fi
    pdflatex -synctex=1 -interaction=nonstopmode $N -output-directory=/home/matteo/Dropbox/
done
