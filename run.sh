#!/bin/bash

#(C) Copyright FORCOAST H2020 project under Grant No. 870465. All rights reserved.

# Copyright notice
# --------------------------------------------------------------------
#  Copyright 2022 Deltares
#   Gido Stoop
#
#   gido.stoop@deltares.nl
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#
#        http://www.apache.org/licenses/LICENSE-2.0
# --------------------------------------------------------------------

# docker run forcoast-sm-a3 ...
INITIAL_DIR="$(pwd)"
cd /usr/src/app
Rscript ./Site_selection_Limfjord_netcdf_V3_mam.R $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12}
gdal_calc.py -A "./Bulletin/oxy.tif" --outfile="./Bulletin/oxy_mgL.tif" --calc="A*(32/1000)" --NoDataValue=-1.0880000445193e+37
python3 ./Bulletin/map_generator_docker.py ${17} ${18} ${19} ${20}
python3 ./Bulletin/send_bulletin.py -A $1 -B $2 -C $3 -D $4 -E $5 -F $6 -G $7 -H $8 -I $9 -J ${10} -K ${11} -L ${12} -M ${13} -N ${14} -O ${15} -P${16}
