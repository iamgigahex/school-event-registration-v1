# Event Registration App

Below are the details on how to setup this project.

### Clone the project
```
git clone https://github.com/iamgigahex/school-event-registration-v1.git
```
# For Docker

Please install docker if not available 

`https://docs.docker.com/desktop/`

## build

Run `docker-compose build`

## Run Server

Run `docker-compose up`

## If you want to run your services in the background

Run `docker-compose up -d`

## Create Admin User

Run `docker-compose run web python manage.py createsuperuser`

## Makemigrations

Run `docker-compose run web python manage.py makemigrations`

## Migrate

Run `docker-compose run web python manage.py migrate`

## To stop your services once you have finished

Run `docker-compose stop`

## To remove all the stopped containers

Run `docker container rm $(docker container ls -aq)`

## To make it easier run docker_run.sh 


Run `./docker_run.sh`


## Setting up and running the application:

### Check if python is installed
```
python ––version
```

### Install Python (skip this if Python is already installed)
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
python ––version
```

### Create the virtual environment and activate it
```
python3 -m venv venv

source venv/bin/activate 
```

For Windows only:
Activate the environment:
```
.\venv\Scripts\activate
```

### Install the requirements
```
pip install -r requirements.txt
```

### Migrate the database
```
python manage.py migrate
```

### Create a new superuser
```
python manage.py createsuperuser
```

### Run the server
```
python manage.py runserver
```

### For accessing the application

```
http://localhost:8000/
http://127.0.0.1:8000/
```

### Sample csv format for uploading participants

```
First Name,Last Name,Profile picture,Email Address,Phone Number,Events
```

### Sample data

```
Sample data availble in /sample_data
```