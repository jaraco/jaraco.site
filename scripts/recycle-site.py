from wmi import GetObject, WMI

server_name = 'teach'
ob = r'winmgmts:{authenticationLevel=pktPrivacy}\\%(server_name)s\root\microsoftiisv2' % vars()
iis = GetObject(ob)
pools = iis.ExecQuery("Select * From IIsApplicationPool")
for pool in pools:
	if 'Primary Web Site' in pool.Name:
		print("Attempting to recycle {0} on {1}".format(pool.Name, server_name))
		pool.Recycle
		break