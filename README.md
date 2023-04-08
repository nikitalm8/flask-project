# Sample Flask Project

## Requirements
- Python 3.9+
- Ubuntu 22+ / Windows 10

## Installation
### Clone repository
```bash
$ git clone
$ cd flask-project/src
```

### Install Python 3.9+ and pip
```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3 python3-pip python3-venv
```

### Setup virtual environment and install dependencies
```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Change `config.yaml` file and secret key
```bash
$ cp config.yaml.example config.yaml
$ vim config.yaml
```

### Setup service
Update `.service` file, then move service file to `/etc/systemd/system/` and reload daemon.
```bash
$ sudo mv flask-site.service /etc/systemd/system/flask-site.service
$ sudo systemctl enable flask-site
$ sudo systemctl start flask-site
```

### Setup nginx
Update `nginx.conf` file, then move config file to `/etc/nginx/sites-available/` and create symlink to `/etc/nginx/sites-enabled/`.
```bash
$ sudo mv nginx.conf /etc/nginx/sites-available/flask-site
$ sudo ln -s /etc/nginx/sites-available/flask-site /etc/nginx/sites-enabled/flask-site
$ sudo systemctl restart nginx
```


## Usage
### If uWSGI is not set up:
```bash
$ cd flask-project/src
$ source env/bin/activate
$ python3 main.py
```
### If uWSGI and nginx are set up:
```bash
$ sudo systemctl restart flask-site
```

## Databases
Using default `SQLite3` database is not recommended for production. It's better to use `PostgreSQL` or `MySQL`. All parameters can be changed in `config.yaml` file.