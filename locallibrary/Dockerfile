# We Use an official Python runtime as a parent image
FROM python:3
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
# create root directory for our project in the container
RUN mkdir /code
# Set the working directory to
WORKDIR /code
# Copy the requirements directory contents into the container at
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
COPY . /code/

# Server
EXPOSE 8080 
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]