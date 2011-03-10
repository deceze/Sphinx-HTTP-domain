from distutils.core import setup

setup(
    name='sphinx-http-domain',
    version='0.1',
    description='Sphinx domain to mark up RESTful web services in ReST',
    url='https://github.com/deceze/Sphinx-HTTP-domain/',
    author='David Zentgraf',
    author_email='deceze@gmail.com',
    py_modules=['sphinx_http_domain'],
    requires=['Spinx'],
    zip_safe=True,
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Documentation'],
)
