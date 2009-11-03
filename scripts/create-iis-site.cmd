@echo off
\windows\system32\inetsrv\appcmd add site /id:3 /name:"Primary Web Site" /physicalPath:c:\inetpub\jaraco.site /bindings:http/*:80:www.jaraco.com,https/*:443:www.jaraco.com
