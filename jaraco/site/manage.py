import os
import shutil

import pkg_resources

def install():
	"""
	Command to install the static content.
	"""
	base = r'\inetpub\jaraco.site'
	os.makedirs(base)
	scripts = ('create-iis-site.cmd isapiapp.py recycle-site.py serve.py '
		'update-site.cmd'.split())
	for script in scripts:
		script_name = 'scripts/' + script
		shutil.copy(pkg_resources.resource_filename('jaraco.site', script_name),
			os.path.join(base, script))
	print "Don't forget you still need to run the scripts in", base
