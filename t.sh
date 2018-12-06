#!/bin/bash

_date=$(date +%F)
_log=output_${_date}.txt
_docroot=/var/www/html/agari
_output=${_docroot}/${_log}
_index=${_docroot}/index.txt

apache_stuff()
# -- Softlink recent
{
unlink ${_index}
ln -s ${_output} ${_index}
}


api_client_id=42c44f7c52d807ecc1d31627a2fc0068807aee52c1ca3cb6303bfa25dae184cd
api_client_secret=3cc62d4239f172bfa6d7016ec91ee6e3067dda37b9065393df9ebfbb4960632a

get_token () {
curl  \
--request POST \
--data "client_id=${api_client_id}&client_secret=${api_client_secret}" \
https://api.agari.com:443/v1/cp/oauth/token 
}

get_users () {
curl --silent -H "Authorization: Bearer $(get_token)" https://api.agari.com:443/v1/cp/users\?pretty\=true\&fields\=full_name,roles \
| jq '.users[] | .full_name, .roles' > ${_output}
}


#-- do it
get_token 
get_users
apache_stuff
