<html>

<head>
<meta name="GENERATOR" content="Microsoft FrontPage 5.0">
<meta name="ProgId" content="FrontPage.Editor.Document">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<title>Password Generator</title>
</head>

<body>
<%@language=Python%>
<%
import codecs, random, itertools, binascii

class nullEncoder( object ):
	def __call__( self, s ):
		return ( s, len( s ) )
		
class pwGen( object ):
	def makePassword( len = 8, encoding = 'base-64' ):
		'Make a password with len bytes of disorder; optionally encoded'
		result = pwGen.getRandChars( len )
		result = ''.join( result )
		if encoding:
			encoder = codecs.getencoder( encoding )
		else:
			encoder = nullEncoder()
		result = encoder( result )
		return result[0]
	makePassword = staticmethod( makePassword )

	def getRandChars( len ):
		return itertools.islice( pwGen.randByteGenerator(), len )
	getRandChars = staticmethod( getRandChars )
	
	def randByteGenerator( ):
		while True:
			yield chr( random.randint( 0, 255 ) )
	randByteGenerator = staticmethod( randByteGenerator )

len = ''
if Request('pwLen').Count:
	len = Request('pwLen')
	newPassword = ''.join( pwGen.getRandChars( int( len ) ) )
	Response.Write( '<P>Your new password is</P><pre>%s</pre>' % binascii.b2a_hex( newPassword ) )
	for encoding in ( 'base-64', ):
		encodedPassword = codecs.getencoder( encoding )( newPassword )[0]
		Response.Write( '<P>Equivalent password (%s) is</P><pre>%s</pre>' % (encoding, encodedPassword ) )
%>

<form action="pwgen.asp">
Password Length (in bytes of disorder): <input name="pwLen" value="<%=len%>"/>
</form>
</body>

</html>