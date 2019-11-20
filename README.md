# django-playground

Playground for Django enabled apps

#django admin-tool
Use the django-admin tool to create the project folder, basic file templates, and project management script (manage.py).

django-admin startproject mytestsite
cd mytestsite

# manage.py

Use manage.py to create one or more applications. We can run the development web server from within this folder using

manage.py and the runserver command, as shown.
\$ python3 manage.py runserver

# References

# 1. deploying to appengine -- nice read

https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35

# 2. Running Django in appengine environment

https://cloud.google.com/python/django/appengine

#Commands for setup

# glcoud init

gcloud auth login
gcloud auth application-default login
gcloud init

# Cloud proxy

# get connection name

gcloud sql instances describe library

# run your proxy

gcloud services enable sqladmin
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances="library-259506:asia-south1:library"=tcp:3306

# Setup

python manage.py makemigrations
python manage.py migrate
python3 manage.py createsuperuser
pip3 freeze > requirements.txt
python manage.py collectstatic

# Deploy to appengine standard environment

gcloud app deploy
