mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
admin:
	python3 manage.py createsuperuser

unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
admin:
	python3 manage.py createsuperuser
remig:
	make unmig
	make faker
	make admin