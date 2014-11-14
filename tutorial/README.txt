Getting started with CherryOnTop
---------------------------------------------------------------------------

This is a quick intro to the features of CherryOnTop and how they can
be useful while building JSON APIs. A few things to keep in mind:

  - These sample apps all exhibit a single controller defined alongside
    the server spin-up code, but you'll notice the controller is never
    explicitly mounted onto the server engine. There is only one
    requirement to ensure routes get mapped: imports for files containing
    controllers must be hit BEFORE the call to `cherryontop.start_server`.

  - Though all handlers in these demos return Python dictionaries, the
    requirement is slightly broader: all handlers must return data that
    can be serialized to JSON.

  - Any config you would normally supply to cherrypy may and should still
    be specified here - socket, port, thread pool size, etc. Setting
    config options on controllers with `_cp_config` still works, too, but
    note that specifying the `request.error_response` key will override
    CherryOnTop's error handling mechanism.
