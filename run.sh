#!/bin/bash
# docker run forcoast-sm-a3 ...

INITIAL_DIR="$(pwd)"

cd /usr/src/app

rscript /usr/src/app/Site_selection_Limfjord_netcdf_V3_mam.R $1 $2

cp /usr/src/app/output/bulletin.png $INITIAL_DIR
