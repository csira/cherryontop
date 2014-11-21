.. image:: https://pypip.in/download/cherryontop/badge.png
    :target: https://pypi.python.org/pypi/cherryontop/
    :alt: Downloads

.. image:: https://pypip.in/version/cherryontop/badge.png
    :target: https://pypi.python.org/pypi/cherryontop/
    :alt: Latest Version

.. image:: https://pypip.in/license/cherryontop/badge.png
    :target: https://pypi.python.org/pypi/cherryontop/
    :alt: License


.. _CherryPy: http://www.cherrypy.org/
.. _Python: http://python.org/


===========
CherryOnTop
===========

CherryOnTop is a library for building JSON API's in Python_ with CherryPy_.

* **Routing:** Built in support for binding static and dynamic URLs alongside the methods that implement their logic (a la Bottle / Flask).
* **Utilities:** Native handling for query parameters, JSON request/response payloads, and error conditions.
* **Server:** All the stability and power of the CherryPy engine.


"Hello world"
-------------

.. code-block:: python

  from cherryontop import Controller, get, start_server

  class HelloWorld(Controller):

      @get('/hello')
      @get('/hello/:name')
      def hello_world(self, name='world'):
          return {'message': 'Hello %s!' % name}

  start_server(<path_to_cherrypy_config>)

Run this script then point your browser to http://localhost:8080/hello/there (or just http://localhost:8080/hello). That's all there is to it.


Download and Install
--------------------

``pip install cherryontop`` to install the latest stable release.


License
-------

.. __: https://github.com/csira/cherryontop/raw/master/LICENSE.txt

Code, tutorials, and documentation all released under the BSD license (see LICENSE__).
