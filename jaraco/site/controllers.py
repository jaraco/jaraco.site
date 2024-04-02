import itertools
import logging

import cherrypy

from jaraco.site.charts import Charts
from jaraco.site.openid import OpenID
from jaraco.site import render, output
from jaraco.site.projecthoneypot import from_cherrypy
from . import resume
from . import landing
from . import projects


log = logging.getLogger(__name__)


class Locator:
    @cherrypy.expose
    def default(self, key):
        if key == 'cu':
            cherrypy.log(f"CU request for {cherrypy.request.remote.ip}")
            raise cherrypy.HTTPRedirect('https://co-opcreditunions.org/locator/')
        raise cherrypy.NotFound()


class Root:
    """
    Create a server:

    >>> root = Root()
    """

    charts = Charts()
    openid = OpenID()
    locate = Locator()
    projects = projects.Projects()

    @cherrypy.expose
    @output('welcome')
    def index(self):
        return render(
            icons=self.icons(),
            meta=dict(
                description="Personal website of Jason R. Coombs",
            ),
            title="jaraco.com",
            name="Jason R. Coombs",
        )

    def icons(self):
        urls = """
            https://github.com/jaraco
            http://stackoverflow.com/users/70170/jason-r-coombs
            https://twitter.com/jaraco
            https://keybase.io/jaraco
            https://linkedin.com/in/jaraco
            https://blog.jaraco.com/
            https://fosstodon.org/@jaraco
            """.split()
        addl = [
            landing.RefIcon(
                'https://pypi.org/user/jaraco',
                """
                <img style="width: 38px; height: 38px; position: relative; top: 15px;"
                src="https://upload.wikimedia.org/wikipedia/commons/0/0a/Python.svg" />
                """,
            )
        ]
        return itertools.chain(map(landing.Icon, urls), addl)

    @cherrypy.expose
    def e5a6ifyiqj_txt(self):
        return "IPv6 confirmed"

    @cherrypy.expose
    def allurbase(self):
        return str(cherrypy.request.base)

    @cherrypy.expose(alias='résumé')
    def resume(self, url=None, emphasis=None):
        return resume.Renderer(url=url, emphasis=emphasis).html()

    @cherrypy.expose(alias='résumé.pdf')
    def resume_pdf(self, url=None, emphasis=None):
        res = resume.Renderer(url=url, emphasis=emphasis).pdf()
        # only set the content type if the rendering succeeded
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        return res

    @cherrypy.expose
    def auth(self):
        return "You authenticated as %s" % cherrypy.request.login

    @cherrypy.expose
    def croakysteel_py(self):
        return from_cherrypy()


class IPTool:
    def __init__(self):
        self.registry = dict()

    @cherrypy.expose
    def register(self, hostname, ip):
        self.registry[hostname] = ip

    @cherrypy.expose
    def report(self):
        return str(self.registry)


class AuthRedirectDemo:
    _cp_config = {
        'tools.auth_basic.on': True,
        'tools.auth_basic.realm': 'jaraco',
        'tools.auth_basic.checkpassword': lambda *args: True,
    }

    @cherrypy.expose
    def here(self):
        raise cherrypy.HTTPRedirect('there/')

    @cherrypy.expose
    def there(self):
        return "You got there!"


Root.ip = IPTool()  # type: ignore
Root.auth_demo = AuthRedirectDemo()  # type: ignore
