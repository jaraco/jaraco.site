# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
	name="jaraco.site",
	use_hg_version=True,
	description="jaraco.com main website",
	author="Jason R. Coombs",
	author_email='jaraco@jaraco.com',
	url='http://bitbucket.org/jaraco/jaraco.site',
	#download_url=download_url,
	license='python',

	install_requires=[
		"CherryPy >= 3.1.2",
		"Genshi >= 0.5.0",
		"lxml >= 2.1.2",
		"isapi-wsgi >= 0.4",
	],
	zip_safe=False,
	packages=find_packages(),
	include_package_data = True,
	namespace_packages=['jaraco'],
	keywords=[
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
	test_suite='nose.collector',
	entry_points = {
	},
	setup_requires = [
		'hgtools',
	],
)
