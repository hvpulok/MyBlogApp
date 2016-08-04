#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import re
from string import letters
# import urllib

# code to initialize google datastore dB
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# >>>>>>>>>>>>>>>>      DB Model definitions     <<<<<<<<<<<<<<<<<<<<<<<<

# Blog DB model
class Blog(db.Model):
    title = db.StringProperty(required= True)
    description = db.TextProperty(required= True)
    created = db.DateTimeProperty(auto_now_add = True)
    lastModified = db.DateTimeProperty(auto_now = True)



# >>>>>>>>>>>>>>>>   Page handler definitions   <<<<<<<<<<<<<<<<<<<<<<<<

# Handler class definition to hadle and render html page request
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Index Page Handler class definition to hadle and render Index html page request
class IndexPage(Handler):
    def render_main(self):
        self.render("index.html")

    def get(self):
        self.render_main()

   

# Blog Page Handler class definition to hadle and render Blog html
class BlogPage(Handler):
    def render_main(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("blogs.html", blogs = blogs)

    def get(self):
        self.render_main()

# Add Blog Page Handler class definition to hadle and render add_blog html page
class AddBlogPage(Handler):
    def render_main(self, title="", description="", error=""):
        self.render("add_blog.html", title=title, description=description, error=error)

    def get(self):
        self.render_main()

    def post(self):
        newBlogTitle =  self.request.get('title')
        newBlogDescription =  self.request.get('description')
        newBlogDescription = newBlogDescription.replace('\n', '<br>')

        if newBlogTitle and newBlogDescription:
            post = Blog(title= newBlogTitle, description=newBlogDescription)
            key = post.put()
            self.redirect("/blog/%s" % key.id())
        else:
            error= "We need both a title and some description of the new blog."
            self.render("add_blog.html", title=newBlogTitle, description=newBlogDescription, error=error)

# New Blog Page Handler class definition to hadle and render add_blog html page
class SelectedBlogPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Blog', int(post_id))
        SelectedBlog = db.get(key)
        self.render("selected_blog.html", blog = SelectedBlog)


# >>>>>>>>>>>>>>>>      Route definitions     <<<<<<<<<<<<<<<<<<<<<<<<
app = webapp2.WSGIApplication([
    ('/', IndexPage),
    ('/blog', BlogPage),
    ('/blog/addblog', AddBlogPage),
    ('/blog/([a-z0-9]+)', SelectedBlogPage)
], debug=True)
