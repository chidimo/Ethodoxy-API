# Ethodoxy API

[![Build Status](https://travis-ci.com/chidimo/Ethodoxy-API.svg?branch=develop)](https://travis-ci.com/chidimo/Ethodoxy-API)
[![Coverage Status](https://coveralls.io/repos/github/chidimo/Ethodoxy-API/badge.svg?branch=develop)](https://coveralls.io/github/chidimo/Ethodoxy-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/a111cd63dfe6f15bd844/maintainability)](https://codeclimate.com/github/chidimo/Ethodoxy-API/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a111cd63dfe6f15bd844/test_coverage)](https://codeclimate.com/github/chidimo/Ethodoxy-API/test_coverage)

Catholic Orthodoxy in electronic format

## URLs

1. Site: <http://chidimo.github.io/Ethodoxy/>
1. API root: <https://ethodoxy.herokuapp.com/api/v1>
1. Swagger documentation: <https://ethodoxy.herokuapp.com/swagger/>

## Available endpoints

1. <https://ethodoxy.herokuapp.com/api/v1/versions/>
1. <https://ethodoxy.herokuapp.com/api/v1/books/>
1. <https://ethodoxy.herokuapp.com/api/v1/chapters/>
1. <https://ethodoxy.herokuapp.com/api/v1/verses/>
1. <https://ethodoxy.herokuapp.com/api/v1/commentary/>

All API endpoint calls have a `count` key which tells the total number of results returned. The actual data is contained in the `results` key.

All results are paginated by `50` pages.

## Recreating the database

It is possible to recreate the database on your local machine as the necessary `.json` files have been included in the `drbo_data` folder. The raw scrapped files are also available in the `drbo_org_scrap` folder.

1. Clone the repo
1. Run `pipenv install` and `pipenv install --dev`
1. Run `python manage.py migrate`
1. Optional. Create superuser with `python manage.py superuser`
1. Optional. Create user with `python manage.py user`
1. Both have the following optional arguments `-email admin@ethodoxy.net -password dwarfstar`
1. Create a `PostgreSQL` database name `ethodoxy-api`.
1. Set up the following environment variables

        DEBUG
        DJANGO_SETTINGS_MODULE=ethodoxy-api.settings.dev
        SECRET_KEY
        EMAIL_HOST_PASSWORD
        EMAIL_PORT
        ALLOWED_HOSTS=localhost
        DATABASE_URL
        DB_PASSWORD

1. Set up **Douay-Rheims** bible database by running the following commands in order

        python manage.py create_version -name -location
        python manage.py create_ot
        python manage.py create_nt
        python manage.py create_chapters
        python manage.py create_verses
        python manage.py create_commentary # challoner commentary

## Contributing

I haven't figured it out yet. Feel free to message me at orjichidi95@gmail.com

## Querying

1. How to query verses
