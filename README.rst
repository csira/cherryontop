.. _CherryPy: http://www.cherrypy.org/
.. _Python: http://python.org/


===========
CherryOnTop
===========

CherryOnTop is a library for building JSON API's in Python_ with CherryPy_.

* **Routing:** Built in support for binding static and dynamic URLs in place (a la Bottle or Flask).
* **Server:** The power and stability of the CherryPy engine.
* **Utilities:** Handling for JSON request/response payloads, descriptive messages and clean propagation for error conditions.


Hello world
-----------

.. code-block:: python

  from cherryontop import get, start_server

  @get("/hello/:name")
  def hello_world(name):
      return {"message": "Hello {}!".format(name)}

  start_server()

Run this script then point your browser to http://localhost:8080/hello/world. That's all there is to it.


Download and Install
--------------------

``pip install cherryontop`` to install the latest stable release.


License
-------

.. __: https://github.com/csira/cherryontop/raw/master/LICENSE.txt

Code, tutorials, and documentation all released under the BSD license (see LICENSE__).
