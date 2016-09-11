#!/usr/bin/env bash
cd /home/matteo/Documenti/workTracker/invoice/
args=${@}
for N in ${args[@]};
do
#    if [[N == 'pdflatex.sh' || N == '' ]]; then
#        break
#    fi
    pdflatex -synctex=1 -interaction=nonstopmode $N
done
