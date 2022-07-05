#!/bin/bash
# docker run forcoast-sm-a3 ...
INITIAL_DIR="$(pwd)"
cd /usr/src/app
Rscript ./Site_selection_Limfjord_netcdf_V3_mam.R $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12}
gdal_calc.py -A "./Bulletin/oxy.tif" --outfile="./Bulletin/oxy_mgL.tif" --calc="A*(32/1000)" --NoDataValue=-1.0880000445193e+37
python3 ./Bulletin/map_generator_docker.py ${17} ${18} ${19} ${20}
python3 ./Bulletin/send_bulletin.py -A $1 -B $2 -C $3 -D $4 -E $5 -F $6 -G $7 -H $8 -I $9 -J ${10} -K ${11} -L ${12} -M ${13} -N ${14} -O ${15} -P${16}
