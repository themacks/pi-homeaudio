#!/usr/bin/python2.7

import webpy.web as web

render = web.template.render('templates/')

urls = (
    '/(.*)', 'index'
)

class index:
    def GET(self, name):
        return render.index(name)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
