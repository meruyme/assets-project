run-migrations:
	docker compose exec web python manage.py makemigrations
	docker compose exec web python manage.py migrate

update-deps:
	docker compose exec web python -m piptools compile -o requirements.txt pyproject.toml

install-deps:
	docker compose exec web pip-sync requirements.txt
	docker compose exec celery pip-sync requirements.txt
	docker compose exec celery-beat pip-sync requirements.txt

local-up:
	docker compose up -d db redis web
	sleep 5
	docker compose exec web python manage.py migrate
	sleep 5
	docker compose up -d celery celery-beat
