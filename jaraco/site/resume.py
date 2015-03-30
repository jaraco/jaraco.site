import urllib.parse
import urllib.request
import os
import subprocess

from lxml import etree

class Renderer:
	url = 'https://dl.dropbox.com'
	url += urllib.parse.quote('/u/54081/Jason R. Coombs resume.xml')

	def __init__(self, url=None):
		if url:
			self.url = url

	def get_transform_path(self, output_name):
		path_tmpl = 'resume-1.5.1/xsl/output/{output_name}.xsl'
		path = path_tmpl.format(**locals())
		here = os.path.dirname(__file__)
		return os.path.join(here, 'static', path)

	def load_url(self):
		"""
		Load self.url and return a readable stream.
		"""
		return urllib.request.urlopen(self.url)

	def html(self):
		transform_path = self.get_transform_path('us-html')
		transform = etree.XSLT(etree.parse(open(transform_path)))
		src = etree.parse(self.load_url())
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
