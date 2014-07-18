Django tutorial at
https://docs.djangoproject.com/en/1.6/intro/

Commands (Run in directory mysite):

* Start test server:
  python manage.py runserver 
 
  -> Application URL: http://127.0.0.1:8000/
  -> Admin URL: http://127.0.0.1:8000/admin

* Sync database:
  python manage.py syncdb

* Run tests:
  python manage.py test polls

Using coverage (see http://nedbatchelder.com/code/coverage/):

* Run coverage like this:
  coverage run --source='.' manage.py test polls

* Show report:
  coverage report
