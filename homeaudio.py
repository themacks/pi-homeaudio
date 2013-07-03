#!/usr/bin/python2.7

import webpy.web as web

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/pandora', 'pandora',
    '/airplay', 'airplay'
)

class index:
    def GET(self):
        return render.index()
        
class pandora:
    def GET(self):
        return "Pandora!"
        
class airplay:
    def GET(self):
        return "Airplay!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
