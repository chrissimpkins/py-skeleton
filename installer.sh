#!/bin/sh

echo " "
echo "Pulling the pyapp archive..."
echo " "
curl -LO https://github.com/chrissimpkins/pyapp/archive/master.tar.gz

echo " "
echo "Unpacking the archive..."
echo " "
tar -xzvf master.tar.gz

echo " "
echo "Preparing project files..."
mv pyapp-master/* .
mv pyapp-master/.gitignore ./.gitignore
mv pyapp-master/.travis.yml ./.travis.yml

echo " "
echo "Cleaning up..."
rm -rf pyapp-master
rm master.tar.gz
rm installer.sh

echo "Complete."
