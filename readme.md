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
