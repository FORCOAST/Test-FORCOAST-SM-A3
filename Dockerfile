FROM r-base

RUN mkdir -p /usr/src/app

RUN mkdir -p /usr/src/app/nc_files_2009
RUN mkdir -p /usr/src/app/nc_files_2010
RUN mkdir -p /usr/src/app/nc_files_2011
RUN mkdir -p /usr/src/app/nc_files_2012
RUN mkdir -p /usr/src/app/nc_files_2013
RUN mkdir -p /usr/src/app/nc_files_2014
RUN mkdir -p /usr/src/app/nc_files_2015
RUN mkdir -p /usr/src/app/nc_files_2016
RUN mkdir -p /usr/src/app/nc_files_2017

COPY . /usr/src/app

COPY ./nc_files_2009 /usr/src/app/nc_files_2009
COPY ./nc_files_2010 /usr/src/app/nc_files_2010
COPY ./nc_files_2011 /usr/src/app/nc_files_2011
COPY ./nc_files_2012 /usr/src/app/nc_files_2012
COPY ./nc_files_2013 /usr/src/app/nc_files_2013
COPY ./nc_files_2014 /usr/src/app/nc_files_2014
COPY ./nc_files_2015 /usr/src/app/nc_files_2015
COPY ./nc_files_2016 /usr/src/app/nc_files_2016
COPY ./nc_files_2017 /usr/src/app/nc_files_2017

RUN apt-get update -y

RUN apt-get install -y libnetcdf-*

RUN Rscript /usr/src/app/install_packages.R

ENTRYPOINT ["/usr/src/app/run.sh"]