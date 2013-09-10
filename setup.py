#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from setuptools import setup, find_packages

setup(
    name='Ximpia',
    version='0.2.0',
    description='Web development environment to speed up your web projects',
    long_description = codecs.open('README.rst', 'r', 'utf-8').read(),
    author='Ximpia Inc',
    author_email='team@ximpia.com',
    url = 'https://ximpia.readthedocs.org',
    download_url='',
    license='Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    scripts=['ximpia/bin/ximpia-app'],
	install_requires=[
		'Django >= 1.4',
        'django-grappelli >= 2.4.4',
        'django-filebrowser >= 3.5.2',
        'South >= 0.7.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False,
)
