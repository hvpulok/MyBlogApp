# Multi User Blog
#### Author: Md Kamrul Hasan Pulok
#### This site is developed as a part of Udacity Full Stack Web Developer Nanodegree Project-3

##Instructions to run the website:
* The website is hosted in Google Cloud Free account, the site can be visited by following this link : http://myblogapp-1470629927816.appspot.com/
* It can also be run using local host: Download Google App Engine python SDK and load this github cloned folder

## Feature Checklist complying Project Rubric: https://review.udacity.com/#!/rubrics/150/view
* Code Functionality:
    * What framework is used? : App is built using Google App Engine : __done__
    * Blog is deployed and viewable to the public : The submitted URL is publicly accessible.: __done__

* Site Usability:
    * The signup, login, and logout workflow is intuitive to a human user : __done__
        * User is directed to login, logout, and signup pages as appropriate. E.g., login page should have a link to signup page and vice-versa; logout page is only available to logged in user. __done__
    * Editing and viewing workflow is intuitive to a human user : __done__
        * Links to edit blog pages are available to users. Users editing a page can click on a link to cancel the edit and go back to viewing that page. : __done__
    * Pages render correctly. Blog pages render properly. Templates are used to unify the site : __done__

* Accounts and Security:
    * User accounts are appropriately handled : __done__
        * Users are able to create accounts, login, and logout correctly : __done__
    * Account information is properly retained : __done__
        * Existing users can revisit the site and log back in without having to recreate their accounts each time. : __done__
    * Usernames are unique : __done__
        * Usernames are unique. Attempting to create a duplicate user results in an error message. : __done__
    * Passwords are secure and appropriately used. : __done__
        * Stored passwords are hashed. Passwords are appropriately checked during login. User cookie is set securely. : __done__

* Permissions:
    * User permissions are appropriate for logged out users. : __done__
        * Logged out users are redirected to the login page when attempting to create, edit, delete, or like a blog post. : __done__
    * User permissions are appropriate for logged in users. : __done__
        * Logged in users can create, edit, or delete blog posts they themselves have created. : __done__
        * Users should only be able to like posts once and should not be able to like their own post. : __done__
    * Comment permissions are enforced. : __done__
        * Users can only edit and delete comments they themselves have made. : __done__