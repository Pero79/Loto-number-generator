#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        besedilo = "Ali zelis generirati 8 nakljucnih loto stevilk?"
        params = {"text":besedilo}
        return self.render_template("index.html", params=params)


class LotoHandler(BaseHandler):
    def get(self):
        return self.render_template("loto.html")

    def post(self):
        random_numbers = random.sample(range(1, 39), 8)
        generate = self.request.get("generate")
        result = 0
        message1 = ""
        message2 = ""

        if generate == "yes":
            message1 = "Here are your numbers:"
            result = str(sorted(random_numbers, key=int))[1:-1]
            message2 = "Good luck! ;)"
        else:
            result="Please press generate or back."


        params = {"result": result, "message1": message1, "message2": message2}
        return self.render_template("loto.html", params=params)





app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/loto', LotoHandler),
], debug=True)
