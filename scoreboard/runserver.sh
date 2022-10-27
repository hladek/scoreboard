# system is configured using django-environ
# copy scoreboard/envtemplate to scoreboard/.env to load env variables from file
SECRET_KEY=zzz DATABASE_URL=sqlite:///db.sqlite3  DEBUG=True python ./manage.py runserver
