# Django-chatbot

This is an AI assitant that allows users to interact with a chatbot/assistant via a web interface. The chatbot is built on the open AI API.

## Usage

--> You can find the live site [here](https://django-chatapp-wm7h.onrender.com/)
### cloning the repository

clone the repository using the command below.
```
git clone git@github.com:jaypee15/django-chatbot.git
```
move into the directory with the files.

```
cd django-chatbot.git
```

create a virtual environment.

```
python -m venv .venv
```

Activate the virtual environment.

```
.venv/scripts/activate
```
create a .env files to store environmental variables and set the following variables to actual values.
```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
OPENAI_API_KEY=
```

install the requirements
```
pip install requirements.txt
```

run migrations
```
python manage.py migrate
```

run tests
```
coverage run manage.py test rooms -v 2
```
start the application
```
python manage.py runserver
```
This will start the chatbot web application. You can then access the application at http://localhost:8000.

App Preview:

![app preview](https://jaypee15.github.io/portfolio/django-chatbot.png)