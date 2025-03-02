import textwrap
from itertools import filterfalse

import cherrypy

from jaraco.develop import filters, git

excludes = [
    '/cherrypy/cheroot',
    '/cherrypy/cherrypy',
    '/pypa/rootbeer',
    '/pypa/wheel',
    'compilers',
    'dotfiles',
    'git-tools',
    'jaraco.github.io',
    'jaraco.pghfreethought',
    'jaraco/tidelift',
    'moneydance',
    'multipy-tox',
    'omaha-data',
    'scicomm.pro',
    'skeleton',
    'twine',
]


def make_url(project):
    return git.resolve(project + '/')


def exclude(project):
    return any(map(make_url(project).__contains__, excludes))


style = textwrap.dedent("""
    @media (prefers-color-scheme: dark) {
      body {
        background-color: #444;
        color: white;
      }
    }
    .container {
      column-width: 20em;
    }
    .container > .project:first-child {
        margin-top: -1.1em;
    }
    .project {
      break-inside: avoid;
      border-left: 1px solid white;
      padding-left: .5em;
    }
    """)


class Projects:
    @cherrypy.expose
    def index(self):
        projects = sorted(
            filterfalse(exclude, filter(filters.Tag('not fork'), git.projects())),
            key=lambda s: s.replace('/', '|'),
        )
        doc = '\n'.join(map(self.make_badge, projects))
        return f'<html><head><style>{style}</style></head><body><div class="container">\n{doc}\n</div></body></html>'

    def make_badge(self, project):
        url = make_url(project)
        badge = url.join('actions/workflows/main.yml/badge.svg').resolved
        workflow = url.join('actions?query=workflow%3A%22tests%22').resolved
        return f'<div class="project"><h3>{project}</h3><a href="{workflow}"><img src="{badge}"></a></div>'
