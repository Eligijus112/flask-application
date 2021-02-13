# flask-application

Putting everything together from this course: https://www.udemy.com/course/rest-api-flask-and-python

# Project summary 

This project uses Flask as a basis to create a REST API to serve a machine learning model. 

This flask application stores a logistic regression model in a database table as a list of features and coefficient values and returns a probability via a GET request. 

Additionally, all the requests are tracked and stored in a database as well. 

# Activating the virtual environment

## With anaconda 

```
conda create python=3.7 flask-api
```

```
conda activate flask-api
```

```
pip install -r requirements.txt
```

## With virtualenv

```
virtualenv flask-api
```

```
source flask-api/bin/activate
```

```
pip install -r requirements.txt
```

# Logistic regression model 

The model is created using the data regarding heart diseases. The project that creates the model can be found via: https://github.com/Eligijus112/heart-disease-model 

# Configurations 

The configurations for the application are stored in a file **.env**. An example file with all the keys is stored in **.env-example** file. 

The cofiguration file includes the port, host name, secret key and other attributes. 

When developing the application, make sure to set the **ENV** parameter to *Dev*.

Example contents of .env file:

```
SECRET_KEY=hello
PORT=5000
HOST=0.0.0.0
ENV=Dev
```

# Launching the application 

To run the application in a testing environment run:

```
python app.py 
```

# Endpoints 

## \<version>/predict 

Predicts the probability of a hear attack given a set of feature values. The request type is **GET**. Features are passed as URL parameters. 

For example:

```
localhost:5000/v1/predict?heartRate=120&glucose=255&BMI=50&totChol=130&cigsPerDay=20&age=55
```

### v1/predict 

Features needed: heartRate, glucose, BMI, totChol, cigsPerDay

### v2/predict 

Features needed: heartRate, glucose, BMI, totChol, cigsPerDay, age

# Manager commands 

The manage commands can be activated using the manage.py script. 

## Uploading the model version to server 

To upload a specific version of a model in a form feature and coefficient pairs use the command:

```
python manage.py add_model <version>
```

# Installing Postgres to server 

The database that stores data about requests to the API is stored in Postgres database. The installation procedure can be found here: 

https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart 

# Running the application using gunicorn and nginx 

The requests are handled and routed by nginx in the server. The application is served using gunicorn. 

The full walkthrough is as follows: 

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
