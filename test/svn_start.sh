#!/bin/bash

# ownership issues, validate...

res=$(docker ps | grep ddb-svn)
svn_stat="$?"

if [[ $svn_stat == 0 ]]; then
    echo "ddb-svn already up"
    exit 0
fi

test/svn_stop.sh

# incase I deleted it from the repo
mkdir -p test/svn_test

echo $(pwd)
# clear old svn stuff
rm test/svn_test/.svn -rf

# start docker
docker run -d  --name ddb-svn -p 80:80 krisdavison/svn-server:v3.0 
sleep 3

# pull empty repo
cd test/svn_test
svn co --no-auth-cache  --username user  --password password http://localhost/svn/SampleProject . --depth empty

# add file
cp ../data/MOCK_DATA.csv .
svn add MOCK_DATA.csv  --no-auth-cache  --username user  --password password
svn commit -m ddb MOCK_DATA.csv  --no-auth-cache  --username user  --password password


