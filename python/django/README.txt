Django tutorial at
https://docs.djangoproject.com/en/1.7/

Commands (Run in directory mysite):

* Database setup
  python manage.py migrate

* Start test server:
  python manage.py runserver 
 
  -> Application URL: http://127.0.0.1:8000/
  -> Admin URL: http://127.0.0.1:8000/admin

* Create the app polls
  python manage.py startapp polls

* Generate migration for app polls
  python manage.py makemigrations polls

* Generate database changes for polls app
  python manage.py sqlmigrate polls 0001

* Run the migration
  python manage.py migrate

* Creating an admin user
  python manage.py createsuperuser

* Start the development server
  python manage.py runserver
