# varastolista
Simple CRUD inventory app for my friend's warehouse using Django.
https://stvl.herokuapp.com/

# Getting started
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Config (optional)
Create .env file

# Running server
python manage.py runserver
python manage.py createsuperuser
python manage.py migrate
