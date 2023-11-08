#
pip install django djangorestframework

#
django-admin startproject easybank .

#
django-admin startapp api

## add into settings.py -- installed_apps
'rest_framework',
'api', // app name

# setup database
create tables

# create superuser
py manage.py createsuperuser
// user: admin
// password: admin
// email: a@b.com

# runserver
py manage.py runserver

# create serializers
create file

# create views
using generics


# create url from the app - api endpoints
new file: urls.py

# insert that new urls.py(from the app) into the urls.py file from the project
include path(endpoints) into the project urls.py file