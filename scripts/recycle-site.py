from wmi import GetObject, WMI

server_name = '.'
ob = r'winmgmts:{authenticationLevel=pktPrivacy}\\{server_name}\root\microsoftiisv2'.format(vars())
iis = GetObject(ob)
pools = iis.ExecQuery("Select * From IIsApplicationPool")
for pool in pools:
	if 'Primary Web Site' in pool.Name:
		print("Attempting to recycle {0} on {1}".format(pool.Name, server_name))
		pool.Recycle
		break