#!/bin/bash

# This bash script will run the blessed plots page generation. Intended to be called
# from a cronjob.


# Configuration
RELEASE="development"
RELEASE_DIR=~/

# Setup nova
echo Setting up test release
source /grid/fermiapp/nova/novaart/novasvn/setup/setup_nova.sh -r ${RELEASE}
pushd ${RELEASE_DIR}/Utilities/BlessedPlots
srt_setup -a

# Get the latest DocDB json file
echo Updating BlessedPlots.json
svn update BlessedPlots.json

# Run the blessed plot maker
echo Running Blessed Plots generation
python RunBlessedPlots.py

# Generate static html
echo Generating html
python make_static_page.py

popd

echo DONE
