FROM r-base

RUN mkdir -p /Test-FORCOAST-SM-A3

RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2009
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2010
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2011
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2012
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2013
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2014
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2015
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2016
RUN mkdir -p /Test-FORCOAST-SM-A3/nc_files_2017

COPY . /Test-FORCOAST-SM-A3

COPY ./nc_files_2009 /Test-FORCOAST-SM-A3/nc_files_2009
COPY ./nc_files_2010 /Test-FORCOAST-SM-A3/nc_files_2010
COPY ./nc_files_2011 /Test-FORCOAST-SM-A3/nc_files_2011
COPY ./nc_files_2012 /Test-FORCOAST-SM-A3/nc_files_2012
COPY ./nc_files_2013 /Test-FORCOAST-SM-A3/nc_files_2013
COPY ./nc_files_2014 /Test-FORCOAST-SM-A3/nc_files_2014
COPY ./nc_files_2015 /Test-FORCOAST-SM-A3/nc_files_2015
COPY ./nc_files_2016 /Test-FORCOAST-SM-A3/nc_files_2016
COPY ./nc_files_2017 /Test-FORCOAST-SM-A3/nc_files_2017

RUN apt-get update -y

RUN apt-get install -y libnetcdf-*

RUN Rscript /Test-FORCOAST-SM-A3/install_packages.R

CMD Rscript /Test-FORCOAST-SM-A3/Site_selection_Limfjord_netcdf_V3_mam.R