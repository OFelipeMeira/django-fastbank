# Installing django and Django-Rest-Framework
**pip install django djangorestframework**

# Create a project
**django-admin startproject easybank .**

# Create the first App
**django-admin startapp api**

# Add into settings.py
```
installed_apps  = [
    'rest_framework',
    'api', // app name
]
```

# Setup database
**create tables**

# Create superuser
```
py manage.py createsuperuser
>> user: admin
>> password: admin
>> email: a@b.com
```

# Runserver
**py manage.py runserver**

# Create serializers
**create file**

# Create views
**using generics**

# Create url from the app - api endpoints
**new file: urls.py**

# Insert that new urls.py(from the app) into the urls.py file from the project
**include path(endpoints) into the project urls.py file**