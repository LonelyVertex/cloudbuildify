start:
	docker-compose up -d --force-recreate --build cloudbuildify


dev:
	FLASK_ENV=development FLASK_APP=cloudbuildify/webhooks.py flask run


install:
	pip install -r requirements.txt
	pip install -e .
