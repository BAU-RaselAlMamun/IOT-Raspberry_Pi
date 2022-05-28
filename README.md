# IOT(Raspberry Pi)
<a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" /></a>

To Create Smart Framing Technology using Raspberry Pi

> - <a href="#environment">1. Environment Setup </a>
> - <a href="#project">2. Project Setup </a>
> - <a href="#skeleton">3. Styling with Skeleton </a>
> - <a href="#dht">4. Setup DHT22 sensor & Show data into Website </a>
> - <a href="#filter">5. Implement data & filter system </a>

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
`$ touch lab_app.py`
```py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```
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

`visit website - http://ip-address`

## 3. Styling with Skeleton <a href="" name="skeleton"> - </a>

`$ mkdir static`\
`$ cd static`\
`$ mkdir css`\
`$ mkdir images`\
`$ mkdir js`

- `Add files- css: normalize.css & skeleton.css & style.css`
- `Add files- images: favicon.png`
- `Add files- js: main.js & jquery-3.6.0.slim.min.js`

`$ mkdir templates`\
`$ touch lab_app.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>

  <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/skeleton.css">
  <link rel="stylesheet" href="static/css/style.css">

  <link rel="icon" type="static/image/png" href="static/images/favicon.png">
</head>
<body>
  <p>Hello World!</p>
  
  <script src="static/js/main.js"></script>
  <script src="static/js/jquery-3.6.0.slim.min.js"></script>
</body>
</html>
```

- Edit File : `lab_app.py`

```py
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route("/")
def lab_app():
    return render_template("lap_app.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

`$ systemctl restart emperor.uwsgi.service`\
`visit website - http://ip-address`

- Debugging a Flask app :

`$ tail -n 100 /var/log/uwsgi/lab_app_uwsgi.log`

## 4. Setup DHT22 sensor & Show data into Website <a href="" name="dht"> - </a>

`$ pip install rpi.gpio`\
`Add - Adafruit_Python_DHT (Copy This Folder)`\
`$ cd Adafruit_Python_DHT/`\
`$ python setup.py install`\
`$ cd examples`\
`$ python AdafruitDHT.py 2302 17` [Note: 2302 - Sensor No. & 17 - GPIO Pin No.]

- Edit File : `lab_app.py`
```py
from flask import Flask, request, render_template
import sys
import Adafruit_DHT

app = Flask(__name__)
app.debug = True

@app.route("/")
def lab_temp():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		return render_template("lab_app.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

- Edit File : `lab_app.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="10">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>Lab App</title>

  <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/skeleton.css">
  <link rel="stylesheet" href="static/css/style.css">

  <link rel="icon" type="static/image/png" href="static/images/favicon.png">
</head>
<body>
  <div class="container">
    <div class="row">
      <div class="two-third column" style="margin-top: 5%">
          <h2>Real time lab conditions</h2>
          <h1>Temperature: {{"{0:0.1f}".format(temp) }}°C</h1>
          <h1>Humidity: {{"{0:0.1f}".format(hum)}}%</h1>  
          <p>This page refreshes every 10 seconds</p>
      </div>   
    </div>
  </div>  

  <script src="static/js/main.js"></script>
  <script src="static/js/jquery-3.6.0.slim.min.js"></script>
</body>
</html>
```
`$ touch template/no_sensor.html`

- Edit File : `no_sensor.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>Lab App</title>

  <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/skeleton.css">
  <link rel="stylesheet" href="static/css/style.css">

  <link rel="icon" type="static/image/png" href="static/images/favicon.png">
</head>
<body>
    <div class='test_container'>
        <h1>Sorry, can't access the sensor!</h1>
    </div>

  <script src="static/js/main.js"></script>
  <script src="static/js/jquery-3.6.0.slim.min.js"></script>
</body>
</html>
```

`$ systemctl restart emperor.uwsgi.service`

### Create Database System

`$ sqlite3 lab_app.db`\
`$ sqlite> begin;`\
`$ sqlite> create table temperatures (rDatetime datetime, sensorID text, temp numeric);`\
`$ sqlite> insert into temperatures values (datetime(CURRENT_TIMESTAMP),"1",25);`\
`$ sqlite> insert into temperatures values (datetime(CURRENT_TIMESTAMP),"1",25.10);`\
`$ sqlite> commit;`\
`$ sqlite> .tables`\
`$ sqlite> select * from temperatures;`\
`$ sqlite> begin;`\
`$ sqlite> create table humidities (rDatetime datetime, sensorID text, hum numeric);`\
`$ sqlite> insert into humidities values (datetime(CURRENT_TIMESTAMP),"1",51);`\
`$ sqlite> insert into humidities values (datetime(CURRENT_TIMESTAMP),"1",51.10);`\
`$ sqlite> commit;`\
`$ sqlite> .tables`

- Add Data into Database:\
`$ touch env_log.py`
```py
import sqlite3
import sys
import Adafruit_DHT

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db') 
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

if humidity is not None and temperature is not None:
	log_values("1", temperature, humidity)	
else:
	log_values("1", 30, 70)
```
`$ python env_log.py`

- Check Data Recording:

`$ sqlite3 lab_app.db`\
`$ sqlite> select * from temperatures;`\
`$ sqlite> select * from humidities;`

- Corn System add:

`$ crontab -e` [Note: Select Editior. Like -1, 2] \
`*/1 * * * * /var/www/lab_app/bin/python /var/www/lab_app/env_log.py` [Note: Add this line & Save It, Here, 1 = 1min.] \
`$ sqlite3 lab_app.db`\
`$ sqlite> select * from temperatures;`\
`$ sqlite> select * from humidities;`

- Show Data into Website:

- Edit File : `lab_app.py`
```py
from flask import Flask, request, render_template
import sys
import Adafruit_DHT
import sqlite3

app = Flask(__name__)
app.debug = True

@app.route("/")
def lab_temp():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		return render_template("lab_app.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db")
def lab_env_db():
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures")
	temperatures = curs.fetchall()
	curs.execute("SELECT * FROM humidities")
	humidities = curs.fetchall()
	conn.close()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

`$ touch templates/lab_env_db.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>Lab App DB</title>
  
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
    <link rel="stylesheet" href="static/css/normalize.css">
    <link rel="stylesheet" href="static/css/skeleton.css">
    <link rel="stylesheet" href="static/css/style.css">
  
    <link rel="icon" type="static/image/png" href="static/images/favicon.png">
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="one-third column" style="margin-top: 5%">
          <strong>Showing all records</strong>                
          <h2>Temperatures</h2>                    
            <table class="u-full-width">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>&deg;C</th>                        
                </tr>
              </thead>
              <tbody>
                {% for row in temp %}
                <tr>
                  <td>{{row[0]}}</td>
                  <td>{{'%0.2f'|format(row[2])}}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>  
            <h2>Humidities</h2>
            <table class="u-full-width">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>%</th>                        
                </tr>
              </thead>
              <tbody>
                {% for row in hum %}
                <tr>
                  <td>{{row[0]}}</td>
                  <td>{{'%0.2f'|format(row[2])}}</td>
                </tr>          
                {% endfor %}
              </tbody>
            </table>                                              
        </div>
      </div>
    </div>
    
    <script src="static/js/main.js"></script>
    <script src="static/js/jquery-3.6.0.slim.min.js"></script>
  </body>
</html>
```
`$ systemctl restart emperor.uwsgi.service`


## 5. Implement data & filter system <a href="" name="filter"> - </a>

`$ sqlite3 lab_app.db`\
`$ sqlite> select * from temperatures;`\
`$ sqlite> select * from humidities;`

- Filter Date & Time:

`$ sqlite> SELECT * FROM temperatures WHERE rDatetime BETWEEN "2022-05-27 14:30:00" AND "2022-05-27 16:30:00";`\
`$ sqlite> SELECT * FROM humidities WHERE rDatetime BETWEEN "2022-05-27 14:30:00" AND "2022-05-27 16:30:00";`

- Edit File : `lab_app.py`
```py
from flask import Flask, request, render_template
import time
import datetime
import sys
import Adafruit_DHT
import sqlite3

app = Flask(__name__)
app.debug = True

@app.route("/")
def lab_temp():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		return render_template("lab_app.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
        from_date_str   = request.args.get('from',time.strftime("%Y-%m-%d %H:%M"))
        to_date_str     = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))

        conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
        curs=conn.cursor()
        curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
        temperatures    = curs.fetchall()
        curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
        humidities      = curs.fetchall()
        conn.close()
        return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

`$ systemctl restart emperor.uwsgi.service`
- Check filter syatem into website : `http://ip-address/lab_env_db?from=2022-05-27 14:30:00&to=2022-05-27 15:30:00`

### Using Invalid Syntex (How it is work?)
- Edit File : `lab_app.py`
```py
from flask import Flask, request, render_template
import time
import sys
import Adafruit_DHT
import datetime
import sqlite3


@app.route("/lab_env_db", methods=['GET']) 
def lab_env_db():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00"))
	to_date_str 	  = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))

	if not validate_date(from_date_str):
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	  = time.strftime("%Y-%m-%d %H:%M")
		
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

`$ systemctl restart emperor.uwsgi.service`\
- Check filter system : `http://ip-address/lab_env_db?from=2022-05-27 14:30:00&to=2022-05-`

### Simplefy the code:
- Edit File : `lab_app.py`
```py
@app.route("/lab_env_db", methods=['GET']) 
def lab_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

def get_records():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00"))
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))

	if not validate_date(from_date_str):
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")	


	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return [temperatures, humidities, from_date_str, to_date_str]
```
`$ systemctl restart emperor.uwsgi.service`

- Edit File : `lab_env_db.html`
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>Lab App DB</title>
  
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
    <link rel="stylesheet" href="static/css/normalize.css">
    <link rel="stylesheet" href="static/css/skeleton.css">
  
    <link rel="icon" type="static/image/png" href="static/images/favicon.png">
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="eleven columns">
          <form id="range_select" action = "/lab_env_db" method="GET">        
            <div class="one column">
              <input type="radio" name="range_h" value="3" id="radio_3" /><label for="radio_3">3hrs</label>
            </div>
            <div class="one column">
              <input type="radio" name="range_h" value="6" id="radio_6" /><label for="radio_6">6hrs</label>
            </div>
            <div class="one column">
              <input type="radio" name="range_h" value="12" id="radio_12" /><label for="radio_12">12hrs</label>
            </div>
            <div class="one column">
              <input type="radio" name="range_h" value="24" id="radio_24" /><label for="radio_24">24hrs</label>
            </div>
          </form>          
        </div>
      </div>
      <div class="row">
        <div class="one-third column" style="margin-top: 5%">
          <strong>Showing all records</strong>
          <h2>Temperatures</h2>
            <table class="u-full-width">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>&deg;C</th>
                </tr>
              </thead>
              <tbody>
                {% for row in temp %}
                <tr>
                  <td>{{row[0]}}</td>
                  <td>{{'%0.2f'|format(row[2])}}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
            <h2>Humidities</h2>
            <table class="u-full-width">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>%</th>
                </tr>
              </thead>
              <tbody>
                {% for row in hum %}
                <tr>
                  <td>{{row[0]}}</td>
                  <td>{{'%0.2f'|format(row[2])}}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
        </div>
      </div>          
    </div>

    <script src="static/js/main.js"></script>
    <script src="static/js/jquery-3.6.0.slim.min.js"></script>
    <script>
      jQuery("#range_select input[type=radio]").click(function(){
        jQuery("#range_select").submit();
      });
    </script>         
  </body>
</html>
```

- Edit File : `lab_app.py`
```py
@app.route("/lab_env_db", methods=['GET']) 
def lab_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

def get_records():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00"))
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))
	range_h_form	= request.args.get('range_h',''); 

	range_h_int 	= "nan"

	try: 
		range_h_int	= int(range_h_form)
	except:
		print ("range_h_form not a number")

	if not validate_date(from_date_str):
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")

	
	if isinstance(range_h_int,int):	
		time_now		    = datetime.datetime.now()
		time_from 	  	= time_now - datetime.timedelta(hours = range_h_int)
		time_to   	  	= time_now
		from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
		to_date_str	    = time_to.strftime("%Y-%m-%d %H:%M")

	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return [temperatures, humidities, from_date_str, to_date_str]
```
`$ systemctl restart emperor.uwsgi.service`