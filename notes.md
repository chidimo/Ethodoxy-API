# Notes

## Local `.env` variables

```.env
DEBUG=
DJANGO_SETTINGS_MODULE=
SECRET_KEY=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587
ALLOWED_HOSTS=localhost, ethodoxy.herokuapp.com
DATABASE_URL=
DB_PASSWORD
```

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


## Vatican II Documents

### Constitutions

    Dei Verbum
    Lumen Gentium
    Sacrosanctum Concilium
    Gaudium et Spes

### Declarations
    Gravissimum Educationis
    Nostra Aetate
    Dignitatis Humanae

### Decrees
    Ad Gentes
    Presbyterorum Ordinis
    Apostolicam Actuositatem
    Optatam Totius
    Perfectae Caritatis
    Christus Dominus
    Unitatis Redintegratio
    Orientalium Ecclesiarum
    Inter Mirifica

## To Do

Scrap topics from drbo.org

Include footnotes and cross-references for haydock

# To scrap

1. <http://www.christianperfection.info/>
1. <https://web.archive.org/web/20180205153812/http://www.christianperfection.info/>
