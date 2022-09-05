## Family budget app

Application for creating and sharing family budgets. Budgets consist of multiple items from different categories.
[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) library is used for authorization. 

### Installation 

1. ```git clone https://github.com/olechanastazja/family_budget.git```
2. ```docker-compose up```

Fixtures should be applied automatically. 

To generate auth token make an HTTP POST request and /api/token `endpoint` e.g.:

**Body:**

`{
	"username": "john",
	"password": "john1"
}`

**Endpoint:**

`http://127.0.0.1:8002/api/token/`

Then grab the access token and go ahead and use of it to GET/POST/PUT/PATCH or DELETE some budgets.

### Tests
To run tests you can either use virtualenv with requirements specified in `requirements.txt` file 
or execute them in a docker container. `pytest` is used so simple:
`` pytest`` should do it. 