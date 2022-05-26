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