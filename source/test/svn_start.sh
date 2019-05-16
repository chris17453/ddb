#!/bin/bash

echo $(pwd)
# clear old svn stuff
rm source/test/svn_test/.svn -rf

# start docker
docker run -d  --name ddb-svn -p 80:80 krisdavison/svn-server:v3.0 

sleep 3
# pull empty repo
cd source/test/svn_test
svn co --no-auth-cache  --username user  --password password http://localhost/svn/SampleProject . --depth empty

# add file
cp ../MOCK_DATA.csv .
svn add MOCK_DATA.csv  --no-auth-cache  --username user  --password password

