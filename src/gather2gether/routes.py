from gather2gether import app
from gather2gether import g2gServer

@app.route('/')
def hello():
    html_ascii_art = '<pre style="white-space: pre-wrap;">'
    for line in g2gServer.get_ascii_art().splitlines():
        html_ascii_art += line + '\n'
    return html_ascii_art + '</pre>'
