# "(C) Copyright FORCOAST H2020 project under Grant No. 870465. All rights reserved."

FROM r-base:4.2.1

RUN apt-get update
RUN apt-get install sudo -y
RUN apt-get install gnupg -y
RUN apt-get install software-properties-common -y
RUN apt-get install wget -y
RUN apt-get install -y libnetcdf-*
RUN apt-get install libgdal-dev -y

RUN wget -O /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x /usr/local/bin/mc
RUN wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | sudo gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN add-apt-repository "deb https://qgis.org/debian $(lsb_release -c -s) main"
RUN DEBIAN_FRONTEND=noninteractive apt-get install qgis -y 
RUN apt install python3-pip -y

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

RUN pip install telepot==12.7
RUN pip install argparse==1.4.0
RUN pip install Pillow==9.2.0
RUN pip install PyQt5==5.15.7

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
RUN mkdir -p /usr/src/app/output
RUN mkdir -p /usr/src/app/Bulletin

COPY . /usr/src/app
COPY ./Bulletin /usr/src/app/Bulletin
COPY ./nc_files_2009 /usr/src/app/nc_files_2009
COPY ./nc_files_2010 /usr/src/app/nc_files_2010
COPY ./nc_files_2011 /usr/src/app/nc_files_2011
COPY ./nc_files_2012 /usr/src/app/nc_files_2012
COPY ./nc_files_2013 /usr/src/app/nc_files_2013
COPY ./nc_files_2014 /usr/src/app/nc_files_2014
COPY ./nc_files_2015 /usr/src/app/nc_files_2015
COPY ./nc_files_2016 /usr/src/app/nc_files_2016
COPY ./nc_files_2017 /usr/src/app/nc_files_2017

RUN Rscript /usr/src/app/install_packages.R

RUN chmod 755 /usr/src/app/run.sh

ENTRYPOINT ["sh", "/usr/src/app/run.sh"]
