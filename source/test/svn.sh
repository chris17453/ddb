# page for svn docker
# https://hub.docker.com/r/krisdavison/svn-server
# thanks!
docker run -d -p 80:80 krisdavison/svn-server:v3.0

# docker exec -it <container-name> bash
# To clear all old users and add a new user simple type. (substitute your user for user-name) and then the system will request that users password.
# 
# htpasswd -c /etc/subversion/passwd user-name
# or to add a new user without removing all the old ones type this. (remove the -c)
# htpasswd /etc/subversion/passwd user-name
#curl --user user:password --include --request PROPFIND --header "Depth: 1" 'http://localhost:80/svn/SampleProject/'


# Another resource 
#add file
#curl -X PUT --anyauth --user 'admin:admin' -T cluster1.xml 'http://localhost:8005/testfile.xml'
#
#make directory
#curl -X MKCOL --anyauth --user 'admin:admin' 'http://localhost:8005/testdir'
#
#move a file
#curl -X MOVE --anyauth --user 'admin:admin' --header 'Destination: http://localhost:8005/testfile1.xml' 'http://localhost:8005/testfile.xml'
#
#list all files in webdav 
#curl --anyauth --user 'admin:admin' -i -X PROPFIND http://localhost:8005/ --upload-file - -H "Depth: 100" <<end
#<?xml version="1.0"?>
#<a:propfind xmlns:a="DAV:">
#<a:prop><a:resourcetype/></a:prop>
#</a:propfind>
#end

#http://svnbook.red-bean.com/
#https://github.com/CloudPolis/webdav-client-python/blob/master/webdav/client.py