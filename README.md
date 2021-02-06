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