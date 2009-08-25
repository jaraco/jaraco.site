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
from jaraco.util import PasswordGenerator
import codecs, binascii

len = ''
if Request('pwLen').Count:
	len = Request('pwLen')
	newPassword = ''.join(PasswordGenerator.get_random_chars(int(len)))
	Response.Write('<P>Your new password is</P><pre>%s</pre>' % binascii.b2a_hex(newPassword))
	for encoding in ('base-64',):
		encodedPassword = codecs.getencoder(encoding)(newPassword)[0]
		Response.Write('<P>Equivalent password (%s) is</P><pre>%s</pre>' % (encoding, encodedPassword))
%>

<form action="pwgen.asp">
Password Length (in bytes of disorder): <input name="pwLen" value="<%=len%>"/>
</form>
</body>

</html>