from setuptools import find_packages, setup


long_desc = '''\
CherryOnTop is a thin layer atop CherryPy that provides convenience methods
for binding routes and handling JSON request/response payloads.
'''


if __name__ == '__main__':
    setup(
        packages=find_packages(),
        name='CherryOnTop',
        version='0.0.2',
        author='Christopher Sira',
        author_email='cbsira@gmail.com',
        license='BSD',
        url='https://github.com/csira/cherryontop',
        description=('Helper abstractions and utilities for building JSON '
                     'APIs with CherryPy.'),
        long_description=long_desc,
        install_requires=[
            'cherrypy',
            'routes',
            'ujson',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Framework :: CherryPy',
            'Intended Audience :: Developers',
            'License :: Freely Distributable',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
