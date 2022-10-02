# Embedathon Website

Django based web application for hosting Embedathon 2022

## Installation Steps for Localhost Setup

If running using Docker Containers, use the following command:

```bash
docker-compose --env-file ./embedathon_website/example.env up
```

### Common Issues

1. If the `start` script cannot be found, ensure that the `LF` line endings are used (uses `CRLF` in Windows by default).

If building the application from scratch, use the following commands:

```bash
pip install -r requirements.txt

mysql -u <username> -p
>> create database embedathon;
>> exit;

cd embedathon_website
cp example.env .env
# fill up the .env file with your local info
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
# open localhost:8000 on your browser
```
