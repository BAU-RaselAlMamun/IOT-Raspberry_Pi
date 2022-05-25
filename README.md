# IOT(Raspberry Pi)
<a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" /></a>

To Create Smart Framing Technology using Raspberry Pi

> - <a href="#environment">1. Environment Setup </a>
> - <a href="#project">2. Project Setup </a>
> - <a href="#skeleton">3. Styling with Skeleton </a>

## 1. Environment Setup <a href="" name="environment"> - </a>


`$ sudo apt-get update`\
`$ sudo apt-get full-upgrade`\
`$ sudo apt-get install build-essential`\
`$ sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev libffi-dev`\
`$ sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libsqlite3-dev libgdbm-dev tk8.5-dev libssl-dev openssl`\
`$ sudo apt-get install libboost-python-dev`\
`$ sudo apt-get install libpulse-dev`\
`$ sudo apt-get install python-dev`\
`$ cd ~`\
`$ mkdir python-source`\
`$ cd python-source/`\
`$ wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz`\
`$ tar zxvf Python-3.10.4.tgz`\
`$ cd Python-3.10.4/`\
`$ ./configure --prefix=/usr/local/opt/python-3.10.4`\
`$ make`\
`$ sudo make install`\
`$ /usr/local/opt/python-3.10.4/bin/python3.10 --version`

## 2. Project Setup <a href="" name="project"> - </a>
`$ sudo su`\
`$ mkdir /var/www`\
`$ mkdir /var/www/lab_app/`\
`$ cd /var/www/lab_app/`\
`$ /usr/local/opt/python-3.10.4/bin/python3.10 -m venv .`\
`$ . bin/activate`\
`$ apt-get install nginx`\
`$ apt-get install sqlite3`\
`$ pip install flask`\
`$ pip install uwsgi`\
`$ rm /etc/nginx/sites-enabled/default`\
`$ touch lab_app_nginx.conf`

```yml
server {
    listen      80;
    server_name localhost;
    charset     utf-8;
    client_max_body_size 75M;

    location /static {
        root /var/www/lab_app/;
    }

    location / { try_files $uri @labapp; }
    location @labapp {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/lab_app/lab_app_uwsgi.sock;
    }
}
```
`$ ln -s /var/www/lab_app/lab_app_nginx.conf /etc/nginx/conf.d/`\
`$ ls -al /etc/nginx/conf.d/`\
`$ /etc/init.d/nginx restart`\
`$ touch lab_app_uwsgi.ini`

```yml
[uwsgi]
base = /var/www/lab_app

app = lab_app
module = %(app)

home = %(base)
pythonpath = %(base)

socket = /var/www/lab_app/%n.sock

chmod-socket    = 666

callable = app

logto = /var/log/uwsgi/%n.log
```
`$ mkdir /var/log/uwsgi`\
`$ bin/uwsgi --ini /var/www/lap_app/lab_app_uwsgi.ini`\
`$ touch /etc/systemd/system/emperor.uwsgi.service`

```yml
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/var/www/lab_app/bin/uwsgi --ini /var/www/lab_app/lab_app_uwsgi.ini

RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

`$ systemctl start emperor.uwsgi.service`\
`$ systemctl status emperor.uwsgi.service`\
`$ systemctl enable emperor.uwsgi.service`\
`$ reboot`

## 3. Styling with Skeleton <a href="" name="skeleton"> - </a>
