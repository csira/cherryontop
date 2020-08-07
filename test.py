from cherryontop import get, start_server

@get("/hello/:name")
def hello_world(name):
    return {"message": f"Hello {name}!"}

start_server(log_to_screen=True, autoreload=True)
