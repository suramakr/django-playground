# django-playground

Playground for Django enabled apps

Setup 
1. django-admin startproject library (Use the django-admin tool to create the project folder, basic file templates, and project management script (manage.py).)
2. cd library

# DEV INSTANCE

1. Postgres database setup
CREATE DATABASE library;
CREATE USER TEST WITH ENCRYPTED PASSWORD 'test123';
\du
grant all privileges on database library to test;
$ psql


2. If you have unapplied migrations, Run 'python manage.py migrate' to apply them.
DJANGO_SETTINGS_MODULE=locallibrary.settings_dev python3 manage.py migrate

3. Run Server
On a dev machine run your Django app with:
DJANGO_SETTINGS_MODULE=locallibrary.settings_dev python3 manage.py runserver


# PROD INSTANCE

On a prod machine run as if you just had settings.py and nothing else.
# glcoud init

gcloud auth login (Ensure you are logged in using credentials for your GCP account) <BR>
gcloud auth application-default login <br>
gcloud init <br>

# Cloud proxy and get connection name

gcloud sql instances describe library <br>

# run your proxy 
# - remember you need postgres drivers - setup if needed for cloud proxy
pip3 install psycopg2-binary <br>
gcloud services enable sqladmin <br>
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64 <br>
chmod +x cloud_sql_proxy <br>

# run cloud proxy
./cloud_sql_proxy -instances="library-259506:asia-south1:library"=tcp:3306 <br>

# Setup

WARNING: python manage.py makemigrations (for first time only)<br>
python manage.py migrate (apply migrations in case of changes)<br>
python3 manage.py createsuperuser<br>
pip3 freeze > requirements.txt<br>
python manage.py collectstatic<br>

# Deploy to appengine standard environment
gcloud app deploy<br>



# KUBERNETES -- managed group of VM instances for running containerized applications.
Assumption: https://console.cloud.google.com/apis/api/container.googleapis.com/overview
Ensure kubernetes engine api is enabled
Instructions: https://cloud.google.com/python/django/kubernetes-engine

# enable cloud sql admin api and install cloud sql proxy
a) gcloud services enable sqladmin
b) wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
c) chmod +x cloud_sql_proxy

# create cloud sql proxy instance and run it for local testing
d) gcloud sql instances describe [YOUR_INSTANCE_NAME]
e) ensure all settings are uptodate with the new connection name
f) ./cloud_sql_proxy -instances="[YOUR_INSTANCE_CONNECTION_NAME]"=tcp:5432

# Creating a service account and proper roles: Cloud SQL Client, Editor + Admin
# Furnish a new private key  and save it as a JSON
Remember to create the json file that has your private key
lib-service created

# Setting up your GKE configuration
0. config check
g) Ensure library.yaml file refers to the proper sql connection names for cloudsqlproxy
h) Note: The one difference between GKE and appengine, is that the static folder needs to 
be created on cloud storage
$gsutil mb gs://gcslibrarybucket
> Creating gs://gcslibrarybucket/...
$gsutil defacl set public-read gs://gcslibrarybucket
> Setting default object ACL on gs://gcslibrarybucket/...
(if not done, python manage.py collectstatic)
Upload the static content to Cloud Storage:
$gsutil rsync -R static/ gs://[YOUR_GCS_BUCKET]/static

In library/settings.py, set the value of STATIC_URL to the following URL, replacing [YOUR_GCS_BUCKET] with your bucket name: for GKE
STATIC_URL = 'http://storage.googleapis.com/[YOUR_GCS_BUCKET]/static/'

# Setup GKE
1. Creating a Kubernetes Engine cluster
gcloud container clusters create library --num-nodes 4

> NAME        LOCATION       MASTER_VERSION  MASTER_IP     MACHINE_TYPE   NODE_VERSION    NUM_NODES  STATUS
librarymgr  asia-south1-b  1.13.11-gke.14  34.93.220.39  n1-standard-1  1.13.11-gke.14  3          RUNNING
 Now that you have created a cluster, you can deploy a containerized application to it.

2. Get authentication credentials for the cluster, make sure kubectl is configured to interact with the right cluster
$ gcloud container clusters get-credentials library

> Fetching cluster endpoint and auth data.
> $ kubeconfig entry generated for library

3. Deploying a containerized web application
Package your app into a Docker container image 
$ gcloud components install kubectl

Make sure the application is packaged as a Docker image, using the Dockerfile that contains instructions on how the image is built.  

4. Setup cloud SQL - You need several secrets to enable your GKE app to connect with your Cloud SQL instance
kubectl delete secret cloudsql-oauth-credentials
kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.json='/Users/sramakrishnan/work/django/django-playground/credentials/library-259506-b97067527626.json' 
>secret/cloudsql-oauth-credentials created

Important step
$kubectl create secret generic cloudsql --from-literal=username=test --from-literal=password=test123


5. Retrieve the public Docker image for the Cloud SQL proxy.
$docker pull b.gcr.io/cloudsql-docker/gce-proxy:1.05

$gcloud sql instances list 
(this will give you and idea of your datbase)
5. Build a Docker image, replacing <your-project-id> with your project ID.
$ docker build -t gcr.io/library-259506/library .
Successfully tagged gcr.io/library-259506/library:latest

Verify your build with 
$docker images
(my_django20_env) admins-MacBook-Pro:locallibrary sramakrishnan$ docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED              SIZE
gcr.io/library-259506/library        latest              b8ae70150f7a        About a minute ago   997MB
python                               3                   0a3a95c81a2b        12 days ago          932MB
b.gcr.io/cloudsql-docker/gce-proxy   1.05                338793fcb60d        3 years ago          10.7MB


$docker system prune (cleanup the space)
$docker container ls -a
$docker container rm <imageid> (if you want to remove images)
$docker system prune -a (to cleanup all unused + cache etc)

8. Configure Docker to use gcloud as a credential helper, so that you can push the image to Container Registry:

$gcloud auth configure-docker
> The following settings will be added to your Docker config file 
located at [/Users/sramakrishnan/.docker/config.json]:
 {
  "credHelpers": {
    "gcr.io": "gcloud", 
    "us.gcr.io": "gcloud", 
    "eu.gcr.io": "gcloud", 
    "asia.gcr.io": "gcloud", 
    "staging-k8s.gcr.io": "gcloud", 
    "marketplace.gcr.io": "gcloud"
  }
}


9. Push the docker image: You create your Docker image and push it to a registry before referring to it in a Kubernetes pod. Kubernetes has native support for the Google Container Registry (GCR), when running on Google Compute Engine (GCE). The kubelet will authenticate to GCR using the instance’s Google service account. T

$ kubectl create deployment libary  --image=gcr.io/library-259506/library:latest
>deployment.apps/libary created
OR
$docker push gcr.io/library-259506/library

Test your docker image
$docker run -p 8000:8000 -i -t <DockerLogin>/<Docker-Image_name>

10. Create the GKE resource:
$ kubectl create -f ./library.yaml 
deployment.extensions/library created
service/library created

Track the status of the deployment:
$kubectl get deployments

11. After the resources are created, there are three polls pods on the cluster. Check the status of your pods:
$ kubectl get pods

debugging
kubectl logs [YOUR_POD_ID]
$ kubectl logs [YOUR_POD_ID] -p
$ kubectl describe pods [library-7f7977fdfc-cvlph]
Crashloop backoff error: https://managedkube.com/kubernetes/pod/failure/crashloopbackoff/k8sbot/troubleshooting/2019/02/12/pod-failure-crashloopbackoff.html
kubectl apply -f ./library.yaml
kubectl get events --sort-by=.metadata.creationTimestamp


Check the state of cluster:
$kubectl get nodes

Check logs in kubectl:
$sudo systemctl status kubectl

12. After the pods are ready, you can get the public IP address of the load balancer:
$kubectl get services library


For incremental updates to yur Dockerfile
 $  docker build -t gcr.io/library-259506/library .
 $  docker push gcr.io/library-259506/library
 $  kubectl apply -f ./library.yaml

# Cleanup
> Delete the Service: This step will deallocate the Cloud Load Balancer created for your Service:
$kubectl delete service hello-web

> Delete the container cluster: This step will delete the resources that make up the container cluster, such as the compute instances, disks and network resources.
$gcloud container clusters delete hello-cluster

# References

# 1. deploying to appengine -- nice read
https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35
and
https://cloud.google.com/python/django/appengine

# 2. Running Django in appengine standard environment
https://cloud.google.com/python/django/appengine

# 3. good threads for dev vs prod
https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings
https://stackoverflow.com/questions/1626326/how-to-manage-local-vs-production-settings-in-django

4. https://postgresapp.com/

5. https://postgresapp.com/

6. app.yaml reference
https://cloud.google.com/appengine/docs/standard/python/config/appref


7. Top reasons for GKE issues 
https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/


8. Kubernetes Cheat Sheet
https://kubernetes.io/docs/reference/kubectl/cheatsheet/#deleting-resources
