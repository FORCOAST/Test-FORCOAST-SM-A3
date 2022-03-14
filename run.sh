#!/bin/bash
# docker run forcoast-sm-a3 ...
INITIAL_DIR="$(pwd)"
cd /usr/src/app
Rscript ./Site_selection_Limfjord_netcdf_V3_mam.R $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12

