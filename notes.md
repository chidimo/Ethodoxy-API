# Notes

## Migrations order

python manage.py makemigrations bible
python manage.py makemigrations siteuser
python manage.py makemigrations commentary
python manage.py makemigrations council
python manage.py makemigrations encyc
python manage.py makemigrations people

python manage.py create_version
python manage.py create_nt
python manage.py create_ot
python manage.py create_chapters
python manage.py create_commentary
python manage.py create_verses

python manage.py create_nt&&python manage.py create_ot&&python manage.py create_chapters&&python manage.py create_commentary&&python manage.py create_verses