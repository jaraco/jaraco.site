import os
import subprocess

from requests_toolbelt import sessions
from lxml import etree


lookup = dict(
    default='/s/sg48j6iuoc819jm/Jason%20R.%20Coombs%20resume.xml?dl=1',
    packaging='/scl/fi/l2xop7gqgz30krxrmx2dw/Jason-R.-Coombs-resume-packaging.xml?rlkey=tm81tcbycqrz6t22t29w92l8j&dl=1',
)


class Renderer:
    session = sessions.BaseUrlSession('https://www.dropbox.com')

    def __init__(self, url=None, emphasis=None):
        self.url = lookup[emphasis or 'default']
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
        print(self.url)
        resp = self.session.get(self.url)
        print(resp.content)
        src = etree.fromstring(resp.content)
        return str(transform(src))

    def pdf(self):
        "use subprocess and fop to render the output"
        cmd = ['fop', '-xml', '-', '-xsl', self.get_transform_path('us-letter'), '-']
        resp = self.session.get(self.url)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate(resp.content)
        return stdout
