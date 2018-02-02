import os
import subprocess
import io

from requests_toolbelt import sessions
from lxml import etree


class Renderer:
	session = sessions.BaseUrlSession('https://dl.dropboxusercontent.com')
	url = '/s/sg48j6iuoc819jm/Jason R. Coombs resume.xml'

	def __init__(self, url=None):
		if url:
			self.url = url

	def get_transform_path(self, output_name):
		path_tmpl = 'resume-1.5.1/xsl/output/{output_name}.xsl'
		path = path_tmpl.format(**locals())
		here = os.path.dirname(__file__)
		return os.path.join(here, 'static', path)

	def html(self):
		transform_path = self.get_transform_path('us-html')
		transform = etree.XSLT(etree.parse(open(transform_path)))
		resp = self.session.get(self.url)
		src = etree.fromstring(resp.content)
		return str(transform(src))

	def pdf(self):
		"use subprocess and fop to render the output"
		cmd = [
			'fop',
			'-xml', '-',
			'-xsl', self.get_transform_path('us-letter'),
			'-',
		]
		data = self.load_url().read()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
			stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate(data)
		return stdout
