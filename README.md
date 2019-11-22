# django-playground

Playground for Django enabled apps

Setup 
1. django-admin startproject library (Use the django-admin tool to create the project folder, basic file templates, and project management script (manage.py).)
2. cd library

# DEV INSTANCE

1. Postgres database setup
CREATE DATABASE library;
CREATE USER TEST WITH ENCRYPTED PASSWORD 'test';
\du
grant all privileges on database library to test;

2. If you have unapplied migrations, Run 'python manage.py migrate' to apply them.
DJANGO_SETTINGS_MODULE=locallibrary.settings_dev python3 manage.py migrate

3. Run Server
On a dev machine run your Django app with:
DJANGO_SETTINGS_MODULE=<your_app_name>.settings_dev python3 manage.py runserver


# PROD INSTANCE

On a prod machine run as if you just had settings.py and nothing else.
# glcoud init

gcloud auth login <br>
gcloud auth application-default login <br>
gcloud init <br>

# Cloud proxy

# get connection name

gcloud sql instances describe library <br>

# run your proxy - remember you need postgres drivers
# Setup if needed for cloud proxy
pip3 install psycopg2-binary <br>
gcloud services enable sqladmin <br>
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64 <br>
chmod +x cloud_sql_proxy <br>
./cloud_sql_proxy -instances="library-259506:asia-south1:library"=tcp:3306 <br>

# Setup

WARNING: python manage.py makemigrations (for first time only)<br>
python manage.py migrate (apply migrations in case of changes)<br>
python3 manage.py createsuperuser<br>
pip3 freeze > requirements.txt<br>
python manage.py collectstatic<br>

# Deploy to appengine standard environment
gcloud app deploy<br>


# References

# 1. deploying to appengine -- nice read
https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35
and
https://cloud.google.com/python/django/appengine

# 2. Running Django in appengine environment
https://cloud.google.com/python/django/appengine

