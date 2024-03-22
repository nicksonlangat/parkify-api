pull:
	git checkout main && git pull
run:
	python manage.py runserver 8005

migrate:
	python manage.py makemigrations && python manage.py migrate

su:
	python manage.py createsuperuser

sort:
	isort accounts core parking_project common
