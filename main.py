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
import hashlib
import hmac
import random
# import urllib

secretCode = "Life is Beautiful"

# code to initialize google datastore dB
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


# >>>>>>>>>>>>>>>>      DB Model definitions     <<<<<<<<<<<<<<<<<<<<<<<<

# ========== User DB model ============
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

# ========== Blog DB model ============
class Blog(db.Model):
    title = db.StringProperty(required= True)
    description = db.TextProperty(required= True)
    created = db.DateTimeProperty(auto_now_add = True)
    lastModified = db.DateTimeProperty(auto_now = True)


# >>>>>>>>>>>>>      Password Protection definitions     <<<<<<<<<<<<<<<<
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secretCode, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)



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

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

# Index Page Handler class definition to hadle and render Index html page request
class IndexPage(Handler):
    def render_main(self):
        self.render("index.html")

    def get(self):
        self.render_main()

   
# ===== Blog  handler definitions =====
# Blog Page Handler class definition to hadle and render Blog html
class BlogPage(Handler):
    def render_main(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        uid = self.read_secure_cookie('user_id')
        if uid:
            key = db.Key.from_path('User', int(uid))
            user = db.get(key)
            self.render("blogs.html", blogs = blogs, currentUser= user.name)
        else:
            self.render("blogs.html", blogs = blogs, currentUser= "")

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

# ===== User handler definitions =====
# ===== username duplicacy check =====
def DuplicateUserFound(username):
    foundUser = User.all().filter('name =', username).get()
    return foundUser

def saveUser(username, password, email):
    # hash password
    pw_hash = make_pw_hash(username, password)

    #save user in dB
    savedUser = User(name= username, pw_hash=pw_hash, email = email)
    key = savedUser.put()
    return User(
            key = key,
            name = username,
            pw_hash = pw_hash,
            email = email)


# signup page Handler
class SignUpPage(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        newUsername = self.request.get('username')
        newEmail = self.request.get('email')
        newPassword1 = self.request.get('password1')
        newPassword2 = self.request.get('password2')
        checkRememberMe = self.request.get('checkRememberMe')

        # code to check password match
        if newPassword1 != newPassword2 :
            error= "Password did not match!"
            self.render("signup.html", username=newUsername, email=newEmail, checkRememberMe=checkRememberMe, error=error)
        elif DuplicateUserFound(newUsername):
            error= "Same Username Already Registered. Please Try different Username"
            self.render("signup.html", username=newUsername, email=newEmail, checkRememberMe=checkRememberMe, error=error)
        else:
            result = saveUser(newUsername, newPassword1, newEmail)
            # resultText = "Thanks. Result : %s %s %s %s" % (result.key, result.username, result.pw_hash, result.email)
            self.write(result.name)

# Login page Handler
class LoginPage(Handler):
    def get(self):
        self.render("login.html")        
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        checkRememberMe = self.request.get('checkRememberMe')

        u = User.all().filter('name =', username).get()
        if u and valid_pw(username, password, u.pw_hash):
            # code to set secure cookie
            val = str(u.key().id())
            cookie_val = make_secure_val(val)
            self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % ('user_id', cookie_val))
            self.redirect('/blog')
            
        else:
            error= "Login Failed due to Username/Password Mismatch"
            self.render("login.html", username=username, checkRememberMe=checkRememberMe, error=error)

class Logout(Handler):
    def get(self):
        # self.logout()
        # clear user-id cookie
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        # redirect to blog page
        self.redirect('/blog')



# >>>>>>>>>>>>>>>>      Route definitions     <<<<<<<<<<<<<<<<<<<<<<<<
app = webapp2.WSGIApplication([
    ('/', IndexPage),
    ('/signup', SignUpPage),
    ('/login', LoginPage),
    ('/logout', Logout),
    ('/blog', BlogPage),
    ('/blog/addblog', AddBlogPage),
    ('/blog/([a-z0-9]+)', SelectedBlogPage)
    
], debug=True)
