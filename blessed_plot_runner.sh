#!/bin/bash

# This bash script will run the blessed plots page generation. Intended to be called
# from a cronjob.


# Configuration
RELEASE="development"
RELEASE_DIR=~/

# Setup nova
echo Setting up LArSoft release
source /grid/fermiapp/products/uboone/setup_uboone.sh
setup uboonecode v06_26_01_01 -q e10:prof

# Get the latest DocDB json file
echo Updating BlessedPlots.json
cp /web/sites/m/microboone-exp.fnal.gov/htdocs/public/approved_plots/BlessedPlots.json .

# Run the blessed plot maker
echo Running Blessed Plots generation
python RunBlessedPlots.py

# Generate static html
echo Generating html
python make_static_page.py

popd

echo DONE
