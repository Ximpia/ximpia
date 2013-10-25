==================
Ximpia Environment
==================

Description
-----------

Ximpia is an agile environment to speed up development of web projects.

On the Front-end, you have visual components with properties defined in HTML5 templates. Server side data is mixed
with components to render final HTML code. Most apps don't need to develop javascript, simply parametrize provided components 
to define visual behavior.

On the server side, you have a service-oriented architecture with views, actions, navigation flow and other server 
services to help speed up development. Services produce JSON data that is processed by visual components.

Documentation
-------------

https://ximpia.readthedocs.org/ 

Installation
------------

Using ``pip``::

	pip install ximpia

This will install ximpia and required packages:

* Grappelli
* Filebrowser
* South

Setup Application
-----------------

To start your application, type::

	ximpia-app myproject.myapp

It will create folders and files needed for your application in ximpia. It will prompt for
basic information like database connection user, admin name and password and locale.

Creates and registers your application home view.

Then you only need to go to directory for your project::

	./manage.py runserver

And open your browser at ``http://127.0.0.1:8000/``

For further details, visit project documentation.

Follow Us
---------
https://www.facebook.com/ximpia
https://twitter.com/ximpia

License
-------

::

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
 
        http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License. 

Copyright (c) 2013 Ximpia Inc
