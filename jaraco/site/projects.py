import textwrap

import cherrypy
from jaraco.develop import git, filters


style = textwrap.dedent("""
    @media (prefers-color-scheme: dark) {
      body {
        background-color: #444;
        color: white;
      }
    }
    """)


class Projects:
    @cherrypy.expose
    def index(self):
        projects = filter(filters.Tag('not fork'), git.projects())
        doc = '<br>\n'.join(map(self.make_badge, projects))
        return f'<html><head><style>{style}</style></head><body>\n{doc}\n</body></html>'

    def make_badge(self, project):
        url = git.resolve(project + '/')
        badge = url.join('actions/workflows/main.yml/badge.svg').resolved
        workflow = url.join('actions?query=workflow%3A%22tests%22').resolved
        return f'<div><a href="{workflow}"><img src="{badge}"></a> {project}</div>'
