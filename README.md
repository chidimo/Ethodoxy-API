# Ethodoxy

Catholic Orthodoxy in electronic format

## API

API root URL: <https://ethodoxy.herokuapp.com/api/v1>

Swagger documentation: <https://ethodoxy.herokuapp.com/swagger/>

## Recreating the database

1. Clone the repo
1. Run `pipenv install` and `pipenv install --dev`
1. Run `python manage.py migrate`
1. Create superuser with `python manage.py superuser`
1. Create user with `python manage.py user`
1. Both have the following optional arguments `-email admin@ethodoxy.net -password dwarfstar`

1. Set up **Douay-Rheims** bible by running the following commands in order
    `python manage.py create_version`
    `python manage.py create_ot`
    `python manage.py create_nt`
    `python manage.py create_chapters`
    `python manage.py create_verses`

1. Set up Challoner commentary by running `python manage.py create_commentary`

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
