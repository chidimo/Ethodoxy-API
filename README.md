# Ethodoxy

## Json files data structure for DR bible

new_test.json and old_test.json `{book name : [book url, book number]}`

chapters folder json files `{book name : {chapter number : chapter url }}`

verses folder json files `{book name-chapter number : {verse number : verse text}}`

How it works

Each verse is a single unit in the database table.

Each underlined item will link to a url. It will pass the following argument `book, chapter, underlined text`

## Recreating the database

1. Clone the repo
1. Run `pipenv install` and `pipenv install --dev`
1. Run `python manage.py migrate`
1. Run `python manage.py shell_plus` to enter an interactive shell
1. Create admin user by running `superuser()`. You can change the associated email from `fixtures/starter.py`
1. Set up **Douay-Rheims** bible by running the following commands in order
    `python manage.py create_version`
    `python manage.py create_ot`
    `python manage.py create_nt`
    `python manage.py create_chapters`
    `python manage.py create_chapters`

1. Run `setup_challoner()` to create the `Challoner` commentary entries.


## Vatican II Documents

# Constitutions
#     Dei Verbum
#     Lumen Gentium
#     Sacrosanctum Concilium
#     Gaudium et Spes

# Declarations
#     Gravissimum Educationis
#     Nostra Aetate
#     Dignitatis Humanae

# Decrees
#     Ad Gentes
#     Presbyterorum Ordinis
#     Apostolicam Actuositatem
#     Optatam Totius
#     Perfectae Caritatis
#     Christus Dominus
#     Unitatis Redintegratio
#     Orientalium Ecclesiarum
#     Inter Mirifica

## To Do

Scrap topics from drbo.org
Include footnotes and cross-references for haydock
