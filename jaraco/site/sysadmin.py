from pythoncom import com_error
import win32com.client

class NTUser(object):
	"A simple class that uses ADSI to change a user's password"
	def __init__(self, userid, system='.'):
		objectString = 'WinNT://%(system)s/%(userid)s,user' % vars()
		try:
			self.user = win32com.client.GetObject(objectString)
		except com_error as exc:
			hr, msg, exc, arg = exc
			if hr==0x8007007b:
				raise ValueError("Account not found or permission denied "
					"locating account.")
			raise ValueError("Unknown error (0x%(hr)x - %(msg)s) opening "
				"%(objectString)s (does IIS user have privilege to Read All "
				"Properties?)" % vars())

	def reset(self, OldPasswd, NewPasswd):
		try:
			self.user.ChangePassword(OldPasswd, NewPasswd)
			# You could use the following instead if you're running under
			# admin privileges self.adsNTUser.SetPassword(NewPasswd)
		except com_error as exc:
			hr, msg, exc, arg = exc
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
			raise ValueError(msg)
