import os
import importlib

import cherrypy
from genshi.core import Stream
from genshi.output import encode, get_serializer
from genshi.template import Context, TemplateLoader

def init():
	return importlib.import_module('jaraco.site.run').app

class DefaultExtensionTemplateLoader(TemplateLoader):
	"""
	A specialized template loader that will append a specific extension
	to each 'load' request if such extension is not present.
	"""
	def __init__(self, *args, **kwargs):
		self.default_extension = kwargs.pop('extension', None)
		if self.default_extension: self.load = self.load_default
		return super(DefaultExtensionTemplateLoader, self).__init__(*args, **kwargs)

	def load_default(self, filename, *args, **kwargs):
		if not filename.endswith(self.default_extension):
			filename += self.default_extension
		return super(DefaultExtensionTemplateLoader, self).load(filename, *args, **kwargs)

loader = DefaultExtensionTemplateLoader(
	os.path.join(os.path.dirname(__file__), 'templates'),
	auto_reload=True,
	extension = '.html',
)

# from the genshi tutorial
def output(filename, method='html', encoding='utf-8', content_type='text/html', **options):
	"""Decorator for exposed methods to specify what template they should use
	for rendering, and which serialization method and options should be
	applied.
	"""
	def decorate(func):
		def wrapper(*args, **kwargs):
			cherrypy.response.headers['Content-Type'] = content_type
			cherrypy.thread_data.template = loader.load(filename)
			opt = options.copy()
			if method == 'html':
				opt.setdefault('doctype', 'html')
			serializer = get_serializer(method, **opt)
			stream = func(*args, **kwargs)
			if not isinstance(stream, Stream):
				return stream
			return encode(serializer(stream), method=serializer,
				encoding=encoding)
		return wrapper
	return decorate

def render(template_name=None, **kwargs):
	"""Function to render the given data to the template specified via the
	``@output`` decorator.
	"""
	if isinstance(template_name, str):
		cherrypy.thread_data.template = loader.load(template_name)
	ctxt = Context(url=cherrypy.url)
	ctxt.push(kwargs)
	return cherrypy.thread_data.template.generate(ctxt)
