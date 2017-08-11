#!/bin/bash

# This bash script will run the blessed plots page generation. Intended to be called
# from a cronjob.


# Configuration
RELEASE="development"
RELEASE_DIR=~/

# File that contains docdb password
export UBDOCPWDFILE=/uboone/app/home/ubooneweb/.ub_docdb_pw.txt

# Setup nova
echo Setting up LArSoft release
source /grid/fermiapp/products/uboone/setup_uboone.sh
setup uboonecode v06_26_01_01 -q e10:prof

# Go in the UBWebPlotHandler directory
cd /uboone/app/home/ubooneweb/UBWebPlotHandler
echo "We are in:"
pwd

# Get the latest DocDB json file
echo Updating BlessedPlots.json
cp /web/sites/m/microboone-exp.fnal.gov/htdocs/public/approved_plots/BlessedPlots.json . 

# Run the blessed plot maker
echo Running Blessed Plots generation
python RunBlessedPlots.py

# Generate static html
echo Generating html
python make_static_page.py

#popd

echo DONE
