@echo off
\windows\system32\inetsrv\appcmd add site /id:3 /name:"Primary Web Site" /physicalPath:c:\inetpub\jaraco.site /bindings:http/*:80:www.jaraco.com,https/*:443:www.jaraco.com
echo "This script does not create an application pool for the site. You must manually create the application pool "Primary Web Site" and connect it to this site