#!/bin/bash
sudo docker-compose down
git pull
sudo docker-compose run web python manage.py makemigrations
sudo docker-compose run web python manage.py migrate
sudo docker-compose up -d