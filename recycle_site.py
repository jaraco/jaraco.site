from wmi import GetObject, WMI

server_name = 'hornigold'
ob = r'winmgmts:{authenticationLevel=pktPrivacy}\\%(server_name)s\root\microsoftiisv2' % vars()
iis = GetObject(ob)
pools = iis.ExecQuery("Select * From IIsApplicationPool")
for pool in pools:
	if 'Primary Web Site' in pool.Name:
		print "Attempting to recycle %s" % pool.Name
		pool.Recycle
		break