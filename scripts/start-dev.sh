python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py migrate django_celery_results

python manage.py runserver 0.0.0.0:8000