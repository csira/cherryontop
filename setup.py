from setuptools import find_packages, setup


# pip install twine
# python setup.py sdist
# twine upload dist/*


long_desc = '''\
CherryOnTop is a small set of utilities and boilerplate for building JSON
API's with CherryPy, it contains convenience methods for route-binding and
some tooling for graceful error propagation. Thanks for taking a look.
'''


if __name__ == "__main__":
    setup(
        packages=find_packages(),
        name="cherryontop",
        version="1.0",
        author="Christopher Sira",
        author_email="cbsira@gmail.com",
        license="BSD",
        url="https://github.com/csira/cherryontop",
        description="Helper utilities for building JSON APIs with CherryPy.",
        long_description=long_desc,
        install_requires=[
            "cherrypy==13.0.0",
            "routes==2.4.1",
            "ujson==1.35"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: CherryPy",
            "Intended Audience :: Developers",
            "License :: Freely Distributable",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
            "Topic :: Software Development :: Libraries :: Python Modules"])
