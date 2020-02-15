from gather2gether import app
from gather2gether import g2gServer

@app.route('/')
def hello():
    htmlAsciiArt = '<pre style="white-space: pre-wrap;">'
    for line in g2gServer.getAsciiArt().splitlines():
        htmlAsciiArt += line + '\n'
    return htmlAsciiArt + '</pre>'
