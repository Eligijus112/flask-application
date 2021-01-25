# flask-application

Putting everything together from this course: https://www.udemy.com/course/rest-api-flask-and-python

# Flask application use

This flask application stores a logistic regression model in a database table as a list of features and coefficient values and returns a probability via a GET request.

# Activating the virtual environment

```
conda create python=3.7 flask-api
```

```
conda activate flask-api
```

```
pip install -r requirements.txt
```

# Definitions

Web server - a piece of software designed to accept incoming web requests.

HTTP verbs - request methods to indicate the desired action to be performed for a given resource.

## Different HTTP verbs

GET
The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.

HEAD
The HEAD method asks for a response identical to that of a GET request, but without the response body.

POST
The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.

PUT
The PUT method replaces all current representations of the target resource with the request payload.

DELETE
The DELETE method deletes the specified resource.

CONNECT
The CONNECT method establishes a tunnel to the server identified by the target resource.

OPTIONS
The OPTIONS method is used to describe the communication options for the target resource.

TRACE
The TRACE method performs a message loop-back test along the path to the target resource.

PATCH
The PATCH method is used to apply partial modifications to a resource.

REST API - a way of thinking about how a web server responds to your requests.

Some features of a REST API:

* The response is not just data but a resource.

* The API is stateless, meaning, one request cannot depend on any other request.

Test first design - Defining the tests/api calls BEFORE starting typing code for API implementation.
