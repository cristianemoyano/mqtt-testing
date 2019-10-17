migrate:
	python manage.py migrate

run:
	python manage.py runserver

migrations:
	python manage.py makemigrations posts

superuser:
	python manage.py createsuperuser

start_mosquitto:
	brew services start mosquitto

stop_mosquitto:
	brew services stop mosquitto

restart_mosquitto:
	brew services restart mosquitto

mqtt:
	python app/cli.py -H localhost -p 1883 -U mosquitto -P mosquitto  -c asgi:application -v