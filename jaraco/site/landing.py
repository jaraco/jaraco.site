import urllib.parse

from importlib.resources import files


class Icon:
    def __init__(self, url):
        self.url = url

    def render(self):
        return f'<a href="{self.url}" target="_top">' \
            f'<span class="icon">{self.image}</span></a>'

    @property
    def image(self):
        source = files('jaraco.site') / 'static' / 'images' / f'{self.name}.svg'
        return source.read_text()

    @property
    def name(self):
        name, _, _ = urllib.parse.urlparse(self.url).netloc.partition('.')
        return name
