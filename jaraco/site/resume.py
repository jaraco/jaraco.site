import urllib.parse
import urllib.request
import os
from lxml import etree

class Renderer:
	url = 'http://dl.dropbox.com' + urllib.parse.quote(
			'/u/54081/Jason R. Coombs resume.xml'
		)

	def __init__(self, url=None):
		if url:
			self.url = url

	def html(self):
		transform_name = os.path.join(
			os.path.dirname(__file__), 'static',
			'resume-1.5.1/xsl/output/us-html.xsl',
			)
		transform = etree.XSLT(etree.parse(open(transform_name)))
		res = urllib.request.urlopen(self.url)
		# TODO: update date_modified in the XML from res.headers
		src = etree.parse(res)
		return str(transform(src))

	def pdf(self):
		# TODO: use subprocess and fop to render the output
		cmd = [
			'fop'
			'-xml', '-',
			'-xsl', transform_name,
			'-',
		]
