from __future__ import absolute_import

from sspi import ClientAuth, ServerAuth

def validate(username, password, domain = ""):
	auth_info = username, domain, password
	ca = ClientAuth("NTLM", auth_info = auth_info)
	sa = ServerAuth("NTLM")

	data = err = None
	while err != 0:
		err, data = ca.authorize(data)
		err, data = sa.authorize(data)
	# If we get here without exception, we worked!

def check(realm, username, password):
	try:
		validate(username, password, realm)
	except Exception:
		return False
	return True