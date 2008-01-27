<%@language=Python%>
<%
Response.ContentType='text/html'

from Ft.Xml.Xslt import Processor
from Ft.Xml import InputSource
from Ft.Lib.Uri import OsPathToUri

import os

def doXMLFile( filename ):
  srcAsUri = OsPathToUri( filename )
  return InputSource.DefaultFactory.fromUri( srcAsUri )

if Request('Name').Count:
	filename = Request('Name')()
else:
	filename =  u'Jason R. Coombs resume.xml'
xmlName = Server.MapPath( filename )
xslName = Server.MapPath( 'resume-1.5.1/xsl/output/us-html.xsl' )

source = doXMLFile( xmlName )
transform = doXMLFile( xslName )

processor = Processor.Processor()

if source and transform:
	processor.appendStylesheet( transform )
	result = processor.run( source )
	Response.Write( result )
%>