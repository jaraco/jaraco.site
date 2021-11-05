import itertools
import logging

import grampg
import cherrypy
import requests

from jaraco.site.charts import Charts
from jaraco.site.openid import OpenID
from jaraco.site import render, output
from jaraco.site.projecthoneypot import from_cherrypy
from . import resume
from . import landing


log = logging.getLogger(__name__)


class Locator:
    @cherrypy.expose
    def default(self, key):
        if key == 'cu':
            cherrypy.log(f"CU request for {cherrypy.request.remote.ip}")
            raise cherrypy.HTTPRedirect('https://co-opcreditunions.org/locator/')
        raise cherrypy.NotFound()


class Downloader:
    @cherrypy.expose
    @output('downloader')
    def index(self):
        return render()

    @cherrypy.expose
    def download(self, name, url, submit):
        filename = name + '.mp4'
        referer = 'http://permaculture.kajabi.com/posts/earthworks-introduction'
        headers = dict(Referer=referer)
        resp = requests.get(url, stream=True, headers=headers)
        resp.raise_for_status()
        cd = 'attachment; filename="{filename}"'.format_map(locals())
        cherrypy.response.headers['Content-Disposition'] = cd
        return resp.iter_content()


class Root(object):
    """
    Create a server:

    >>> root = Root()
    """

    charts = Charts()
    openid = OpenID()
    downloader = Downloader()
    locate = Locator()

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

    @cherrypy.expose
    def resume(self, url=None):
        return resume.Renderer(url).html()

    @cherrypy.expose
    def resume_pdf(self, url=None):
        res = resume.Renderer(url).pdf()
        # only set the content type if the rendering succeeded
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        return res

    @cherrypy.expose
    def auth(self):
        return "You authenticated as %s" % cherrypy.request.login

    @cherrypy.expose
    def croakysteel_py(self):
        return from_cherrypy()


class AcctMgmt(object):
    @cherrypy.expose
    @output('Account Management')
    def index(self):
        return render()

    @cherrypy.expose
    @output('Change Password')
    def change_password(
        self,
        submit,
        username,
        old_password,
        new_password,
        new_password_confirm,
        system=None,
    ):
        from jaraco.site.sysadmin import NTUser

        try:
            if not new_password:
                raise ValueError("Blank passwords not allowed")
            if not new_password == new_password_confirm:
                raise ValueError("Passwords don't match")
            nt = NTUser(username, system or '.')
            nt.reset(old_password, new_password)
        except ValueError as e:
            response_messages = ['Password change has failed.', str(e)]
        else:
            response_messages = [
                'Password change for {nt.user.FullName} was successful!'.format(
                    **vars()
                )
            ]
        return render(response_messages=response_messages)

    @cherrypy.expose
    @output('password gen')
    def password_gen(self, length=None):
        if length is None:
            return render(password=None, length=8)
        length = int(length)
        return render(password=self._gen_password(length), length=length)

    @staticmethod
    def _gen_password(length):
        """
        >>> pw = AcctMgmt._gen_password(10)
        >>> len(pw)
        10
        """
        gengen = grampg.PasswordGenerator()
        gen = gengen.of().some('alphanumeric').length(length).done()
        return gen.generate()


class IPTool(object):
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


Root.acctmgmt = AcctMgmt()
Root.ip = IPTool()
Root.auth_demo = AuthRedirectDemo()
