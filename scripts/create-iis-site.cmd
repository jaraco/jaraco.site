@echo off
\windows\system32\inetsrv\appcmd add site /id:3 /name:"Primary Web Site" /physicalPath:c:\inetpub\jaraco.site /bindings:http/*:80:www.jaraco.com,https/*:443:www.jaraco.com
\windows\system32\inetsrv\appcmd add apppool /name:"Primary Web Site"
\windows\system32\inetsrv\appcmd set app "Primary Web Site/" /applicationPool:"Primary Web Site"
mkdir \inetpub\jaraco.site
