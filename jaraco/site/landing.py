import urllib.parse

from importlib_resources import files
from genshi.builder import tag
from genshi.core import Markup


class IconBase:
    def __init__(self, url):
        self.url = url

    def render(self):
        return tag.a(href=self.url, target='_top', rel='me')(
            tag.span(Markup(self.image), class_='icon')
        )

    @property
    def name(self):
        name, _, _ = urllib.parse.urlparse(self.url).netloc.partition('.')
        return name


class Icon(IconBase):
    @property
    def image(self):
        source = files('jaraco.site') / 'static' / 'images' / f'{self.name}.svg'
        return source.read_text()


class RefIcon(IconBase):
    def __init__(self, url, image):
        self.url = url
        self.image = image
