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

	transform_path = os.path.join(
		os.path.dirname(__file__), 'static',
		'resume-1.5.1/xsl/output/us-html.xsl',
		)

	def html(self):
		transform = etree.XSLT(etree.parse(open(self.transform_path)))
		res = urllib.request.urlopen(self.url)
		# TODO: update date_modified in the XML from res.headers
		src = etree.parse(res)
		return str(transform(src))

	def pdf(self):
		# TODO: use subprocess and fop to render the output
		cmd = [
			'fop',
			'-xml', '-',
			'-xsl', self.transform_path.replace('us-html', 'us-letter'),
			'-',
		]
		res = urllib.request.urlopen(self.url)
		data = res.read()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
			stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate(data)
		return stdout
