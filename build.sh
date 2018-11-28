#!/bin/bash
dir=$(pwd)
pub="$1"


if [[ $PIPENV_ACTIVE -ne '1' ]];
then
    if [[ $BUILD_O -ne 1 ]];
    then
        export BUILD_O=1
        echo "Going Deeper  -> pipenv shell"
        pipenv run ./build.sh $pub
        exit 0
    fi
fi



echo "Attempting to PyPi package"

echo "Remove old images"
if [[ ! -d 'dist' ]];
then
    mkdir dist
fi

cd dist
rm *.gz -f
cd ..

if [[ ! -d '.git' ]];
then
    git init
fi
echo "Adding git changes"
git add -A 
git commit -m 'Bump Version'

echo "Bumping Python patch version"
bumpversion patch --allow-dirty
if [[ $? -ne 0 ]]; then
    
    ver="$(pipenv run pip show pip | grep Version)"
    echo $ver
#    if [[ "$ver" != "Version: 18.0" ]];
#    then
#        echo "reinstall"
#        pipenv install pip==18
#    fi
    
    pipenv install bumpversion pip==18

cat >.bumpversion.cfg <<EOL
[bumpversion]
current_version = 1.0.0 
files = setup.py
commit = False
tag = False 
EOL



git commit -m 'BumpVersion Config'

fi

echo "Build the package"
python setup.py sdist

echo "---$pub"
if [[ ! -z "$pub" ]]; then
    echo "Upload the package"
    twine upload  dist/*
fi

if [[ ! -d 'test' ]];
then
    mkdir test
fi

echo "Updating test Environment"
cd test
pipenv install "$dir"
cd ..


echo "Done.."