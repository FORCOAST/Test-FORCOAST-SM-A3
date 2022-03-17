#!/bin/bash
# docker run forcoast-sm-a3 ...
INITIAL_DIR="$(pwd)"
cd /usr/src/app
Rscript ./Site_selection_Limfjord_netcdf_V3_mam.R $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${16} ${17} ${18}
python3 ./Bulletin/send_bulletin.py -A $1 -B $2 -C $3 -D $4 -E $5 -F $6 -G $7 -H $8 -I $9 -J ${10} -K ${11} -L ${12} -M ${13} -N ${14} -O ${15} 
