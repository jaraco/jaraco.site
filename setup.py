#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

needs_wheel = {'release', 'bdist_wheel', 'dists'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'jaraco.site'
description = 'jaraco.com main website'

setup_params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=name.split('.')[:-1],
	zip_safe=False,
	install_requires=[
		"CherryPy",
		"Genshi",
		"lxml",
		"svg.charts",
		'requests',
		'more_itertools',
		'grampg',
	],
	extras_require={
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	] + wheel,
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
	],
	entry_points={
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
