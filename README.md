# varastolista
An inventory app for my friend's warehouse  
https://stvl.herokuapp.com/

# Stack
Backend written in Python using the Django web framework  
Frontend is custom HTML & CSS built with jQuery  
QR code reader created with Instascan  
https://github.com/schmich/instascan

Hosted on Heroku.

# Getting started
## 1. Make sure you have a recent version of Python 3 installed  
https://www.python.org/

## 2. Use pip (Python package manager) to install packages
Either ```pip install``` or ```pip3 install``` depending on your Python installation

## 3. Install virtualenv (Python virtual environment tool)
```pip install virtualenv```  

## 4. Create a virtual environment named venv
```virtualenv venv```

## 5. Activate virtual environment
On Linux  
```source venv/bin/activate```

On Windows  
```source venv/Scripts/activate```

## 6. Upgrade pip to latest version
```pip install --upgrade pip```  

## 7. Install other required packages while virtual environment is active
```pip install -r requirements.txt```

# Config
Create a file called .env in the project root folder with the following content

## Mandatory
### Secret key (any random string of characters will do)
```DJANGO_SECRET_KEY=qwerty123```

## Non-mandatory
### To use a different database than SQLite
```DATABASE_URL=[your database url here]```

### To send out email alarms (eg. from a gmail account)
```EMAIL_HOST_USER=[your email username here]```   
```EMAIL_HOST_PASSWORD=[your email password here]```  
```STVL_EMAILEES=[recipients email addresses here separated by a space]```

# Running the backend locally
Commands should start with either ```python``` or ```python3``` depending on your installation

## Execute migrations
```python manage.py migrate```

## Create a superuser
```python manage.py createsuperuser```

## Run server
```python manage.py runserver```

## Open in browser
http://localhost:8000