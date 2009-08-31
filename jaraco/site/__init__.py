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
		'tools.trailing_slash.on': True,
		'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
	})

	app = cherrypy.tree.mount(Root(), '/', {
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static',
			'tools.staticdir.content_types': dict(svg='image/svg+xml'),
		}
	})

	return app

loader = TemplateLoader(
	os.path.join(os.path.dirname(__file__), 'templates'),
	auto_reload=True
)

# from the genshi tutorial
def output(filename, method='html', encoding='utf-8', **options):
	"""Decorator for exposed methods to specify what template they should use
	for rendering, and which serialization method and options should be
	applied.
	"""
	if not filename.endswith('html'): filename=filename+'.html'
	def decorate(func):
		def wrapper(*args, **kwargs):
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

def render(*args, **kwargs):
	"""Function to render the given data to the template specified via the
	``@output`` decorator.
	"""
	if args:
		assert len(args) == 1, \
			'Expected exactly one argument, but got %r' % (args,)
		template = loader.load(args[0])
	else:
		template = cherrypy.thread_data.template
	ctxt = Context(url=cherrypy.url)
	ctxt.push(kwargs)
	return template.generate(ctxt)
