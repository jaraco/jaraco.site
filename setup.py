from setuptools import setup, find_packages

setup_params = dict(
	name="jaraco.site",
	use_hg_version=True,
	description="jaraco.com main website",
	author="Jason R. Coombs",
	author_email='jaraco@jaraco.com',
	url='http://bitbucket.org/jaraco/jaraco.site',
	license='python',
	install_requires=[
		"CherryPy>=3.2.3,<4dev",
		"Genshi>=0.5.0",
		"lxml>=2.1.2",
		"isapi-wsgi>=0.4",
		"svg.charts",
		'jaraco.util>=5.0.1',
		"six",
	],
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
			'jaraco-site-install = jaraco.site.manage:install',
			'jaraco-site-reset-bindings = jaraco.site.manage:reset_bindings',
		],
	),
	setup_requires = [
		'hgtools',
	],
)

if __name__ == '__main__':
	setup(**setup_params)
