import os
import cherrypy
from genshi.core import Stream
from genshi.output import encode, get_serializer
from genshi.template import Context, TemplateLoader

def init():
	from jaraco.site.controllers import Root
	cherrypy.config.update({
		'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
		'tools.decode.on': True,
		'tools.sessions.on': True,
		'tools.trailing_slash.on': True,
		'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
	})

	import jaraco.site.sspi
	basic_auth = {
		'tools.auth_basic.on': True,
		'tools.auth_basic.realm': 'jaraco.com',
		'tools.auth_basic.checkpassword': jaraco.site.sspi.check,
	}

	app = cherrypy.tree.mount(Root(), '/', {
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static',
			'tools.staticdir.content_types': dict(svg='image/svg+xml'),
		},
		'/auth': basic_auth,
		'/openid/server': basic_auth,
	})

	return app

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
	if isinstance(template_name, basestring):
		cherrypy.thread_data.template = loader.load(template_name)
	ctxt = Context(url=cherrypy.url)
	ctxt.push(kwargs)
	return cherrypy.thread_data.template.generate(ctxt)
