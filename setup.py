import sys

from setuptools import setup, find_packages

py26_reqs = ['importlib'] if sys.version_info < (2, 7) else []

setup_params = dict(
	name="jaraco.site",
	use_hg_version=True,
	description="jaraco.com main website",
	author="Jason R. Coombs",
	author_email='jaraco@jaraco.com',
	url='http://bitbucket.org/jaraco/jaraco.site',
	license='python',
	install_requires=[
		"CherryPy >= 3.2.3dev-20120408, <3.3dev",
		"Genshi >= 0.5.0",
		"lxml >= 2.1.2",
		"isapi-wsgi >= 0.4",
		"svg.charts",
		'jaraco.util>=5.0.1',
	] + py26_reqs,
	zip_safe=False,
	packages=find_packages(),
	include_package_data = True,
	namespace_packages=['jaraco'],
	keywords=[
	],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
	entry_points = dict(
		console_scripts = [
			'install-jaraco-site = jaraco.site.manage:install',
		],
	),
	setup_requires = [
		'hgtools',
	],
	dependency_links = [
		'http://dl.dropbox.com/u/54081/cheeseshop/index.html',
	],
	use_2to3=True,
)

if __name__ == '__main__':
	setup(**setup_params)
