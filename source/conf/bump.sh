
raw_version_file='./source/conf/version'
python_version_file='./source/ddb/version.py'

v=$(cat ./source/conf/$raw_version_file)

echo "VERION="$v
exit
#put it in the main coinfig file
echo "${v%.*}.$((${v##*.}+1))">$raw_version_file

#update the version in the py file
echo "__version__='${v%.*}.$((${v##*.}+1))'">$python_version_file

 
