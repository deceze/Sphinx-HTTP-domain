import os

from distutils.core import setup


with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='sphinx-http-domain',
    version='0.2',
    description='Sphinx domain to mark up RESTful web services in ReST',
    long_description=long_description,
    url='https://github.com/deceze/Sphinx-HTTP-domain/',
    author='David Zentgraf',
    author_email='deceze@gmail.com',
    packages=['sphinx_http_domain'],
    requires=['Sphinx'],
    zip_safe=True,
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Documentation'],
)
