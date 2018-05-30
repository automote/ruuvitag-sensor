'''
Get data from sensors and write it to InfluxDB

Requires:
    influxdb - pip install influxdb


** Docker InfluxDB & Grafana guide **

Download container
$ docker pull samuelebistoletti/docker-statsd-influxdb-grafana

Create and start new container
$ docker run -d --name docker-statsd-influxdb-grafana -p 3003:3003 -p 3004:8083 -p 8086:8086 -p 22022:22 -p 8125:8125/udp samuelebistoletti/docker-statsd-influxdb-grafana:latest

Or start existing container
$ docker start docker-statsd-influxdb-grafana

InfluxDB: http://localhost:3004/

First create new table: CREATE TABLE tag_data
Query to return all tag data: SELECT * FROM ruuvitag
Remove all data: DROP SERIES FROM ruuvitag

Grafana: http://localhost:3003/ (root/root)

Add datasource (type: InfluxDB url: http://localhost:8086, database: tag_data)
Add new graph to dashboard
'''

from influxdb import InfluxDBClient
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import time

def convert_to_influx(mac, payload):
    return {
        "measurement": "ruuvitag",
        "tags": {
            "mac": mac
        },
        "fields": {
            "temperature": payload["temperature"],
            "humidity": payload["humidity"],
            "pressure": payload["pressure"],
	    "battery" : payload["battery"],
	    "acc_X"   : payload["acceleration_x"],
	    "acc_Y"   : payload["acceleration_y"],
	    "acc_Z"   : payload["acceleration_z"],
	    "counter" : payload["movement_counter"],
	    "tx_power": payload["tx_power"]
        }
    }


client = InfluxDBClient(host="localhost", port=8086, database="tag_data")

count = 0
print("sending data")
'''
sensor = RuuviTag(mac)

while True:
    data = sensor.update()
'''
while True:
	try:
		print("reading Data")
		#datas = RuuviTag.update()
		datas = RuuviTagSensor.get_data_for_sensors(macs='EE:A1:C8:AF:34:5D')
		print(datas)		
		print("reading Done")
		json_body = [convert_to_influx(mac, payload) for mac, payload in datas.items()]
		client.write_points(json_body)
		print("sending successful")
		print(count)
		count = count + 1
	except:
        	print("sending failed")
'''    
	# Wait for 2 seconds and start again
	try:
		time.sleep(2)
	except KeyboardInterrupt:
		print('Exit')
		break
'''

