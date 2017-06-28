import cherrypy


def get_header(name):
    return cherrypy.request.headers.get(name)


def set_header(name, value):
    cherrypy.response.headers[name] = value




def get_cookie(name):
    cookie = cherrypy.request.cookie.get(name)
    return cookie.value if cookie else None


def set_cookie(name, val, **morsels):
    c = cherrypy.response.cookie
    c[name] = val
    for k, v in morsels.iteritems():
        c[name][k] = v
