
v=$(cat version)

#put it in the main coinfig file
echo "${v%.*}.$((${v##*.}+1))">./source/conf/version

#update the version in the py file
echo "__version__='${v%.*}.$((${v##*.}+1))'">./source/ddb/version.py

 
