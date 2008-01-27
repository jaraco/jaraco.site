<html>

<head>
<meta name="GENERATOR" content="Microsoft FrontPage 5.0">
<meta name="ProgId" content="FrontPage.Editor.Document">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<title>Password Change</title>
</head>

<body>

<%@language=Python%>
<%
import pythoncom
import win32com.client

def Respond( s ):
	Response.Write( s + '<br/>\n' )

class NTUser:
# Uses ADSI to change password under user privileges	
	def __init__(self, userid, system='.'):
		objectString = 'WinNT://%(system)s/%(userid)s,user' % vars()
		try:
			self.user = win32com.client.GetObject( objectString )
		except pythoncom.com_error, (hr,msg,exc,arg):
			if hr==0x8007007b:
				raise ValueError, "Account not found or permission denied locating account."
			raise ValueError, "Unknown error (0x%(hr)x - %(msg)s) opening %(objectString)s (does IIS user have privilege to Read All Properties?)" % vars()

	def reset(self, OldPasswd, NewPasswd):
		try:
			self.user.ChangePassword(OldPasswd, NewPasswd)
			# You could use the following instead if you're running under admin privileges
			# self.adsNTUser.SetPassword(NewPasswd)
		except pythoncom.com_error, (hr, msg, exc, arg):
			scode = hex(exc[5])
			if (scode == "0x8007005"):
				msg = "Your NT Account is locked out."
			elif (scode == "0x80070056"):
				msg = "Invalid Old NT Password."
			elif (scode == "0x800708ad"):
				msg = "The specified NT Account does not exist."
			elif (scode == "0x800708c5"):
				msg = "Your new password does not meet the policy requirements for passwords on this system."
			else:
				msg = "ADSI Error - 0x%(hr)x: %(msg)s, %(scode)s" % vars()
			raise ValueError, msg

username = str(Request('username'))
system = str(Request('system'))
newpw1 = str(Request('newpw1'))
newpw2 = str(Request('newpw2'))
oldpw = str(Request('oldpw'))

try:
	if not newpw1:
		raise ValueError, "Blank passwords not allowed"
	if not newpw1 == newpw2:
		raise ValueError, "Passwords don't match"
	nt = NTUser(username,system or '.')
	nt.reset(oldpw,newpw1)
except ValueError, message:
	Respond( "Password change has failed." )
	Respond( str( message ) )
else:
	name = nt.user.FullName
	Respond( 'Password change for %(name)s was successful!' % vars() )


%>
</body>

</html>